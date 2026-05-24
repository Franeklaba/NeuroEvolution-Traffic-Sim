import numpy as np
from .layer import Layer

class AiAgent:
    def __init__(self, ml_input_type):
        if ml_input_type == 1:
            self.hidden_layer = Layer(input_size=11, output_size=15)
            self.output_layer = Layer(input_size=15, output_size=2)
        elif ml_input_type == 2:
            self.hidden_layer = Layer(input_size=18, output_size=21)
            self.output_layer = Layer(input_size=21, output_size=2)
        elif ml_input_type == 3:
            self.hidden_layer = Layer(input_size=25, output_size=27)
            self.output_layer = Layer(input_size=27, output_size=2)
        elif ml_input_type == 4:
            self.hidden_layer = Layer(input_size=32, output_size=36)
            self.output_layer = Layer(input_size=36, output_size=2)
        elif ml_input_type == 5:
            self.hidden_layer = Layer(input_size=18, output_size=21)
            self.output_layer = Layer(input_size=21, output_size=2)
        else:
            raise ValueError(f"Invalid ml_input_type: {ml_input_type}")
        

    def forward(self, inputs):

        inputs_array = np.array(inputs, ndmin=2)

        hidden_output = self.hidden_layer.forward_relu(inputs_array)
        raw_output = self.output_layer.forward_linear(hidden_output)

        raw_steering = raw_output[:, 0]
        raw_acceleration = raw_output[:, 1]

        steering = np.tanh(raw_steering)        
        acceleration = np.tanh(raw_acceleration) 

        return np.column_stack((steering, acceleration))


    def get_network_genes(self):
        h_w, h_b = self.hidden_layer.get_layer_weights()
        o_w, o_b = self.output_layer.get_layer_weights()
        return [h_w, h_b, o_w, o_b]

    def set_network_genes(self, genes):
        self.hidden_layer.set_layer_weights(genes[0], genes[1])
        self.output_layer.set_layer_weights(genes[2], genes[3])