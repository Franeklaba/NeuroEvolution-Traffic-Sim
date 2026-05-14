from Car_simulation import CarSimulationMenager
from Sim_ai_agent import AiAgent

class TrainingManager:
    simulation_time: int = 400
    population_size = 4
    generations = 3

    def __init__(self):
        self.simulation_menager = CarSimulationMenager(is_trainig_mode=False)
        self.ai_agent = AiAgent(self.population_size)


    def run(self):
        for _ in range(self.generations):
            fitness_scores = [0 for _ in range(self.population_size)]
            for i in range(self.population_size):
                self.simulation_menager.reset()
                self.simulation_menager.step(0, [[0]])
                for frame in range(self.simulation_time):
                    
                    actions_matrix = self.ai_agent.get_neuron_output(i, self.simulation_menager.get_ml_input())
                    self.simulation_menager.step(frame, actions_matrix)
                    if not self.simulation_menager.is_active():
                        break
                fitness_scores[i] = self.simulation_menager.get_score()
            self.ai_agent.reproduction_and_evolve(fitness_scores)
        
        self.simulation_menager.quit()
        
        
