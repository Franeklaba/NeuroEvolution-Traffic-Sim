from Car_simulation import CarSimulationMenager
from Sim_ai_agent import AiAgent
from sim_func import *
import argparse
simulation_time = 3000
population_size = 100
generations = 100

simulation_menager = CarSimulationMenager(is_trainig_mode=False)
ai_agents = [AiAgent() for _ in range(population_size)]

ai_agents = load_gens(ai_agents)
for _ in range(generations):
    fitness_scores = [0 for _ in range(population_size)]
    for i in range(population_size):
        for map_type in simulation_menager.config.map_types:
            fitness_scores[i] += run_single_simulation(simulation_menager, ai_agents[i], map_type)
    reproduction_and_evolve(ai_agents, fitness_scores)
save_gens(ai_agents)
simulation_menager.quit()
