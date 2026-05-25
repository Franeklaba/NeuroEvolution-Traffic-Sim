from Car_simulation import CarSimulationMenager
from Sim_ai_agent import AiAgent
import numpy as np
import queue
import csv

from neuroevolutionconfig import NEURO_EVOLUTION_CONFIG, NeuroevolutionConfig 


def run_single_simulation(simulation_manager: CarSimulationMenager, ai_agent: AiAgent, map_type="track"):
    simulation_manager.reset(map_type)
    for frame in range(NEURO_EVOLUTION_CONFIG.simulation_time):
        observations = simulation_manager.get_ml_input()
        actions_matrix = ai_agent.forward(observations)
        simulation_manager.step(frame, actions_matrix)
        if not simulation_manager.is_active():
            break
    return simulation_manager.get_score()
def run_simulation(simulation_manager: CarSimulationMenager, ai_agent: AiAgent):
    scores = np.array([run_single_simulation(simulation_manager, ai_agent, m) for m in simulation_manager.config.map_types])
    # return min(scores) 
    return np.mean(scores) - (NEURO_EVOLUTION_CONFIG.stability_penalty_weight * np.std(scores))
def evaluate_genes(genes):
    simulation_manager = CarSimulationMenager(1, is_trainig_mode=True)
    local_agent = AiAgent(1)
    local_agent.set_network_genes(genes)
    
    score = run_simulation(simulation_manager, local_agent)
    
    simulation_manager.quit() 
    return score
def mutate_genes(genes, mutation_rate=NEURO_EVOLUTION_CONFIG.base_mutation_rate / 2, mutation_strength=NEURO_EVOLUTION_CONFIG.base_mutation_strength / 2):
    mutated_genes = []
    for chromosome in genes:
        new_gene = chromosome.copy()
        mask = np.random.rand(*new_gene.shape) < mutation_rate
        noise = np.random.normal(0, mutation_strength, size=new_gene[mask].shape)
        new_gene[mask] += noise
        mutated_genes.append(new_gene)
        
    return mutated_genes

def reproduction_and_evolve(agents: list[AiAgent], neurons_results):
    num_elites = 5
    csv_filename = NEURO_EVOLUTION_CONFIG.result_file_path
    
    scores = np.array(neurons_results)
    sorted_results_idx = np.argsort(scores)[::-1]
    elite_indices = [idx for idx in sorted_results_idx[:num_elites]]
    best_score = scores[sorted_results_idx[0]]
    overall_mean = scores.mean()
    
    top_10_percent_count = max(1, len(agents) // 10)
    best_individuals_avg_score = np.mean(scores[sorted_results_idx[:top_10_percent_count]])
    print(f"Najlepszy agent: {best_score:.2f} | Średnia Top 10%: {best_individuals_avg_score:.2f} | Średni wynik: {overall_mean:.2f}")

    with open(csv_filename, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([best_score, best_individuals_avg_score, overall_mean])
    best_genes = agents[elite_indices[0]].get_network_genes()
    new_population_genes = []
    for idx in elite_indices:
        new_population_genes.append(agents[idx].get_network_genes())

    shifted_scores = scores - scores.min() + 1e-6
    probabilities = shifted_scores / shifted_scores.sum()
    remaining_count = len(agents) - num_elites
    parent_indices = np.random.choice(len(agents), size=remaining_count, p=probabilities)

    progress = max(0.0, min(1.0, best_individuals_avg_score / NEURO_EVOLUTION_CONFIG.target_score))
    mutation_rate = NEURO_EVOLUTION_CONFIG.base_mutation_rate * (1.1 - progress)
    mutation_strength = NEURO_EVOLUTION_CONFIG.base_mutation_strength * (1.1 - progress)

    for idx in parent_indices:
        genes = agents[idx].get_network_genes()
        mutated_genes = mutate_genes(genes, mutation_rate, mutation_strength)
        new_population_genes.append(mutated_genes)
    
    for i in range(len(agents)):
        agents[i].set_network_genes(new_population_genes[i])
        
    return best_genes
def load_gens(agents : list[AiAgent]):
    weights_file_path = NEURO_EVOLUTION_CONFIG.weights_file_path
    try:
        geny = np.load(weights_file_path, allow_pickle=True)
    except FileNotFoundError:
        return agents
    for i in range(len(agents)):
        agents[i].set_network_genes(geny[i])
    return agents
    
    
def save_gens(agents : list[AiAgent], best_genes):
    weights_file_path = NEURO_EVOLUTION_CONFIG.weights_file_path
    geny = [agent.get_network_genes() for agent in agents]
    np.save(weights_file_path, np.array(geny, dtype=object))
    best_weights_file_path = NEURO_EVOLUTION_CONFIG.best_weights_file_path
    np.save(best_weights_file_path, np.array(best_genes, dtype=object))


def render_best_agent(gene_queue):
    simulation_manager = CarSimulationMenager(1, is_trainig_mode=False) 
    local_agent = AiAgent(1)
    
    while True:
        latest_genes = gene_queue.get() 
        try:
            while True:
                next_genes = gene_queue.get_nowait() 
                latest_genes = next_genes
        except queue.Empty:
            pass
        if latest_genes == "STOP":
            break
        local_agent.set_network_genes(latest_genes)
        run_simulation(simulation_manager, local_agent)
    simulation_manager.quit()