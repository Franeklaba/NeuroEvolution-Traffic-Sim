import numpy

class Layer:
    def __init__(self, input_size: int, output_size: int):
        """
        Inicjalizacja warstwy. Wagi są losowane z rozkładu normalnego,
        a biasy inicjowane jako zera.
        """
        self.weights = numpy.random.randn(input_size, output_size) * 0.1
        self.biases = numpy.zeros((1, output_size))

    def forward(self, inputs: numpy.ndarray) -> numpy.ndarray:
        """
        Przejście "do przodu". Zwraca wyjście z danej warstwy, które jest
        przekazywane do następnej (lub stanowi końcową decyzję).
        """
        # inputs to macierz [1 x input_size]
        # weights to macierz [input_size x output_size]
        # output to macierz [1 x output_size]
        output = numpy.dot(inputs, self.weights) + self.biases
        return self._activation_function(output)

    def _activation_function(self, x: numpy.ndarray) -> numpy.ndarray:
        """
        Funkcja aktywacji. Tu zastosowano tangens hiperboliczny (Tanh),
        który zwraca wartości z zakresu od -1.0 do 1.0 (idealne dla np. kierownicy).
        """
        return numpy.tanh(x)
