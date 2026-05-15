import numpy as np
class Neuron:
    def __init__(self):
        self.weight = np.random.randn() * 0.1
        self.bias = np.random.randn() * 0.1
    def mutate(self, strength):
        self.bias += np.random.randn() * strength
        self.weight += np.random.randn() * strength

    def set_weigth_bias(self,w,b):
        self.bias = b
        self.weight = w

    def get_z(self, x):
        return x * self.weight + self.bias
