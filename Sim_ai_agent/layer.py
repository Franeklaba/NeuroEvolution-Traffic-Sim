import numpy as np

class Layer:
    def __init__(self, input_size, output_size):
        self.weights = np.random.uniform(-1, 1, (input_size, output_size))
        self.biases = np.zeros((1, output_size))

    def forward_linear(self, inputs):
        return np.dot(inputs, self.weights) + self.biases

    def forward_relu(self, inputs):
        linear_output = self.forward_linear(inputs)
        return np.maximum(0, linear_output)

    def get_layer_weights(self):
        return self.weights, self.biases

    def set_layer_weights(self, new_weights, new_biases):
        self.weights = new_weights
        self.biases = new_biases