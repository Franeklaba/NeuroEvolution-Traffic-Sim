from .neuron import Neuron
import random
class AiAgent:
    def activate_func(self, z):
        return 1 if z > 0 else 0

    def __init__(self, population):
        self.population = population
        self.neurons = [Neuron() for _ in range(self.population)]

    def get_neuron_output(self, k, x):
        z = self.neurons[k].get_z(x)
        return self.activate_func(z)
    
    def reproduction_and_evolve(self, neurons_results):
        best_three_neurons_idx = []
        for i in range(3):
            best_three_neurons_idx.append(neurons_results.index(max(neurons_results)))
            neurons_results[best_three_neurons_idx[len( neurons_results) - 1]] = -float('inf')

        new_neurons = []
        for neuron_idx in best_three_neurons_idx:
            new_neurons.append[self.neurons[neuron_idx].weight, self.neurons[neuron_idx].bias]

        for i in range(3):
            self.neurons[i].set_weigth_bias(*new_neurons[i])

        for i in range(3, len(self.neurons)):
            idx = random.randint(0, 2)
            self.neurons[i].set_weigth_bias(*new_neurons[idx])
            self.neurons[i].mutate(0.1)
        


    