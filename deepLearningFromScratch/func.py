import numpy as np


class NeuralNetwork:
    def __init__(self):
        self.layers = []
        self.activations = {
            'sigmoid': self.sigmoid,
            'tanh': self.tanh,
            'relu': self.relu,
            'softmax': self.softmax
        }

    @staticmethod
    def sigmoid(x):
        return 1 / (1 + np.exp(-x))

    @staticmethod
    def tanh(x):
        return np.tanh(x)

    @staticmethod
    def relu(x):
        return np.maximum(x, 0)

    @staticmethod
    def softmax(x):
        exps = np.exp(x - np.max(x, axis=1, keepdims=True))
        return exps / np.sum(exps, axis=1, keepdims=True)

    def dense(self,number_of_neurons , activation_function , input_shape = None):
        if not self.layers and input_shape is None:
            raise ValueError("İlk katman ise girdi shape i vermelisiniz")
        input_dim = input_shape or self.layers[-1]['weights'].shape[1]
        w = np.random.randn(input_dim , number_of_neurons) * 0.01
        b = np.zeros((1, number_of_neurons))

        self.layers.append({"weights": w, "bias": b, "activation_function": activation_function})

    def forward(self, X):
        current_input = X
        for layer in self.layers:
            weights = layer['weights']
            bias = layer['bias']
            activation = self.activations[layer['activation_function']]
            current_input = activation(np.dot(current_input,weights) + bias)

        return current_input





