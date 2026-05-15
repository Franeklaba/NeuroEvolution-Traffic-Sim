import numpy as np
from .layer import Layer

class AiAgent:
    def __init__(self):
        self.hidden_layer = Layer(input_size=9, output_size=12)
        self.output_layer = Layer(input_size=12, output_size=2)

    def forward(self, inputs):

        inputs_array = np.array(inputs, ndmin=2)

        hidden_output = self.hidden_layer.forward_relu(inputs_array)
        raw_output = self.output_layer.forward_linear(hidden_output)

        raw_steering = raw_output[:, 0]
        raw_acceleration = raw_output[:, 1]

        steering = np.tanh(raw_steering)        
        
        sigmoid_accel = 1 / (1 + np.exp(-raw_acceleration))
        acceleration = np.where(sigmoid_accel > 0.5, 1, 0)

        return np.column_stack((steering, acceleration))


    def get_network_genes(self):
        h_w, h_b = self.hidden_layer.get_layer_weights()
        o_w, o_b = self.output_layer.get_layer_weights()
        return [h_w, h_b, o_w, o_b]

    def set_network_genes(self, genes):
        self.hidden_layer.set_layer_weights(genes[0], genes[1])
        self.output_layer.set_layer_weights(genes[2], genes[3])