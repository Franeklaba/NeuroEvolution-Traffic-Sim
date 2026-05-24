from Car_simulation import CarSimulationMenager
from Sim_ai_agent import AiAgent
from sim_func import *
import multiprocessing
from multiprocessing import Process, Queue

from neuroevolutionconfig import NEURO_EVOLUTION_CONFIG, NeuroevolutionConfig 

population_size = NEURO_EVOLUTION_CONFIG.population_size
generations = NEURO_EVOLUTION_CONFIG.generations
ml_input_types = [1,2,3,4,5]


if __name__ == '__main__':
    ai_agents = [AiAgent(1) for _ in range(population_size)]
    ai_agents = load_gens(ai_agents)
    
    cores = max(1, multiprocessing.cpu_count() - 1) 
    gene_queue = Queue()
    render_process = Process(target=render_best_agent, args=(gene_queue,))
    render_process.start()

    for gen in range(generations):
        population_genes = [agent.get_network_genes() for agent in ai_agents]
        with multiprocessing.Pool(processes=cores) as pool:
            fitness_scores = pool.map(evaluate_genes, population_genes)  
        best_genes = reproduction_and_evolve(ai_agents, fitness_scores, 'ml_input_1_results.csv')
        gene_queue.put([layer.copy() for layer in best_genes])
        
        print(f"Zakończono generację {gen + 1}")
        
    save_gens(ai_agents)

    gene_queue.put("STOP")
    render_process.join()