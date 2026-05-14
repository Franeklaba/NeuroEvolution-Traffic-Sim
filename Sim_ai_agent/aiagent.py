from .neuron import Neuron
import random
class AiAgent:
    def activate_func(self, z):
        return 1 if z > 0 else 0

    def __init__(self, population):
        self.population = population
        self.neurons = [Neuron() for _ in range(self.population)]

    def get_neuron_output(self, k, x):
        z = self.neurons[k].get_z(x[0][0])
        return [[self.activate_func(z)]]
    
    def reproduction_and_evolve(self, neurons_results):
        num_elites = 3
        
        indexed_results = list(enumerate(neurons_results))
        indexed_results.sort(key=lambda x: x[1], reverse=True)
        elite_indices = [idx for idx, score in indexed_results[:num_elites]]

        best_idx = elite_indices[0]
        print(f"Najlepszy neuron -> Waga: {self.neurons[best_idx].weight:.4f}, Bias: {self.neurons[best_idx].bias:.4f}, Wynik: {indexed_results[0][1]}")

        new_population_genes = []
        for idx in elite_indices:
            new_population_genes.append((self.neurons[idx].weight, self.neurons[idx].bias))

        min_score = min(neurons_results)
        if min_score <= 0:
            shifted_scores = [score - min_score + 1e-5 for score in neurons_results]
        else:
            shifted_scores = neurons_results

        remaining_count = len(self.neurons) - num_elites
        parent_indices = random.choices(range(len(self.neurons)), weights=shifted_scores, k=remaining_count)

        for idx in parent_indices:
            new_population_genes.append((self.neurons[idx].weight, self.neurons[idx].bias))

        for i in range(len(self.neurons)):
            self.neurons[i].set_weigth_bias(*new_population_genes[i])
        for i in range(num_elites, len(self.neurons)):
            self.neurons[i].mutate(0.1)
        


    