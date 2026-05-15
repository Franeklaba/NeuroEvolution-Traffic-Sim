from Car_simulation import CarSimulationMenager
from Sim_ai_agent import AiAgent
from sim_func import run_single_simulation, reproduction_and_evolve

simulation_time = 500
population_size = 30
generations = 100

simulation_menager = CarSimulationMenager(is_trainig_mode=False)
ai_agents = [AiAgent() for _ in range(population_size)]

for _ in range(generations):
    fitness_scores = [0 for _ in range(population_size)]
    for i in range(population_size):
        simulation_menager.reset()
        fitness_scores[i] = run_single_simulation(simulation_menager, ai_agents[i])
    reproduction_and_evolve(ai_agents, fitness_scores)

simulation_menager.quit()