import numpy as np

class NeuralNetwork:
    def __init__(self, input_size=7, hidden_size=8, output_size=4):
        self.input_size = input_size
        self.hidden_size = hidden_size
        self.output_size = output_size
        self.num_weights = (input_size * hidden_size) + (hidden_size * output_size)

    def act(self, inputs, weights):

        w1_end = self.input_size * self.hidden_size
        w1 = weights[:w1_end].reshape(self.input_size, self.hidden_size)
        w2 = weights[w1_end:].reshape(self.hidden_size, self.output_size)

        hidden = np.tanh(np.dot(inputs, w1))
        output = np.tanh(np.dot(hidden, w2))

        directions = [(0, -1), (0, 1), (-1, 0), (1, 0)]
        move = directions[np.argmax(output)]
        return move
