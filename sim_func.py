from Car_simulation import CarSimulationMenager
from Sim_ai_agent import AiAgent
import numpy as np
simulation_time = 1000

def run_single_simulation(simulation_manager: CarSimulationMenager, ai_agent: AiAgent):
    for frame in range(simulation_time):
        observations = simulation_manager.get_ml_input()
        actions_matrix = ai_agent.forward(observations)
        simulation_manager.step(frame, actions_matrix)
        if not simulation_manager.is_active():
            break
    return simulation_manager.get_score()


import numpy as np

def mutate_genes(genes, mutation_rate=0.1, mutation_strength=0.1):
    mutated_genes = []
    for chromosome in genes:
        new_gene = chromosome.copy()
        mask = np.random.rand(*new_gene.shape) < mutation_rate
        noise = np.random.normal(0, mutation_strength, size=new_gene[mask].shape)
        new_gene[mask] += noise
        mutated_genes.append(new_gene)
        
    return mutated_genes

def reproduction_and_evolve(agents : list[AiAgent], neurons_results):
    num_elites = 3
    scores = np.array(neurons_results)
    sorted_results_idx = np.argsort(scores)[::-1]
    elite_indices = [idx for idx in sorted_results_idx[:num_elites]]

    print(f"Najlepszy neuron -> : {scores[sorted_results_idx[0]]}")

    new_population_genes = []
    for idx in elite_indices:
        new_population_genes.append(agents[idx].get_network_genes())

    shifted_scores = scores - scores.min() + 1e-6
    probabilities = shifted_scores / shifted_scores.sum()
    remaining_count = len(agents) - num_elites
    parent_indices = np.random.choice(len(agents), size=remaining_count, p=probabilities)

    for idx in parent_indices:
        genes = agents[idx].get_network_genes()
        mutated_genes = mutate_genes(genes)
        new_population_genes.append(mutated_genes)
    
    for i in range(len(agents)):
        agents[i].set_network_genes(new_population_genes[i])
