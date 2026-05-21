from Car_simulation import CarSimulationMenager
from Sim_ai_agent import AiAgent
from sim_func import *
import multiprocessing
from multiprocessing import Process, Queue
import queue

simulation_time = 3000
population_size = 100
generations = 40

def render_best_agent(gene_queue):
    simulation_manager = CarSimulationMenager(is_trainig_mode=False) 
    local_agent = AiAgent()
    
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
if __name__ == '__main__':
    ai_agents = [AiAgent() for _ in range(population_size)]
    ai_agents = load_gens(ai_agents)
    
    cores = max(1, multiprocessing.cpu_count() - 1) 
    gene_queue = Queue()
    render_process = Process(target=render_best_agent, args=(gene_queue,))
    render_process.start()

    for gen in range(generations):
        population_genes = [agent.get_network_genes() for agent in ai_agents]
        
        with multiprocessing.Pool(processes=cores) as pool:
            fitness_scores = pool.map(evaluate_genes, population_genes)
            
        best_genes = reproduction_and_evolve(ai_agents, fitness_scores)
        gene_queue.put([layer.copy() for layer in best_genes])
        
        print(f"Zakończono generację {gen + 1}")
        
    save_gens(ai_agents)

    gene_queue.put("STOP")
    render_process.join()