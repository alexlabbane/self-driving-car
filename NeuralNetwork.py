import numpy as np
from random import randint, random

from numpy.random import rand
import pygame
from pygame import draw

def sigmoid(lst):
    return 1 / (1 + np.exp(-lst))

def relu(lst):
    for i in range(len(lst)):
        lst[i] = max(0, lst[i])

    return lst

class Layer:

    def __init__(self, n_neurons, next_layer=None):
        self.num_neurons = n_neurons
        self.next_layer = next_layer

        self.biases = np.zeros((n_neurons,))

        if next_layer != None:
            self.weights = np.random.uniform(low=-3, high=3, size=(self.next_layer.num_neurons, n_neurons))      
        else:
            self.weights = []

    def cross(self, partner):
        if randint(0, 8) == 1:
            mutation_rate = 10
        else:
            mutation_rate = 100000000 # Infinity

        child_layer = Layer(self.num_neurons)

        if self.next_layer != None:
            child_layer.weights = np.zeros((len(self.weights), len(self.weights[0])))
        
        child_layer.biases = np.zeros((len(self.biases),))

        if self.next_layer != None:
            for i in range(len(self.weights)):
                for j in range(len(self.weights[i])):
                    p = randint(0, 100) / 100
                    if p > 0.5:
                        child_layer.weights[i][j] = self.weights[i][j]
                    else:
                        child_layer.weights[i][j] = partner.weights[i][j]

                    # Mutate
                    if randint(0, mutation_rate) == 1:
                        child_layer.weights[i][j] += (4 * random()) - 2

        for i in range(len(self.biases)):
            p = randint(0, 100) / 100
            child_layer.biases[i] = p * self.biases[i] * (1 - p) * partner.biases[i]
            
            # Mutate
            if randint(0, mutation_rate) == 1:
                child_layer.biases[i] += (4 * random()) - 2

        return child_layer

    # Activations are the "inputs" to the layer; how activated each neuron is
    def propagate(self, activations: list[float]):
        if self.next_layer == None:
            return sigmoid(np.array(activations) + self.biases)
        
        activations = relu(np.array(activations) + self.biases)

        next_layer_activations = []

        for partial_sums in np.multiply(self.weights, activations):
            next_layer_activations.append(np.sum(partial_sums))

        if self.next_layer != None:
            return self.next_layer.propagate(next_layer_activations)

class NeuralNetwork:

    def __init__(self, n_inputs, n_outputs, n_hidden=[]):
        self.n_inputs = n_inputs
        self.n_ouputs = n_outputs
        self.n_hidden = n_hidden

        self.output_layer = Layer(n_outputs)
        
        self.layers: list[Layer] = [None for i in range(2 + len(n_hidden))]

        self.layers[-1] = self.output_layer
        layer_counter = 1

        for num_neurons in n_hidden:
            self.layers[-1 - layer_counter] = Layer(num_neurons, self.layers[-layer_counter])
            layer_counter += 1
        
        self.input_layer = Layer(n_inputs, self.layers[1])
        self.layers[0] = self.input_layer

    def think(self, inputs):
        return self.input_layer.propagate(inputs)

    def cross(self, partner):
        child_network = NeuralNetwork(self.n_inputs, self.n_ouputs, self.n_hidden)

        child_network.output_layer = self.output_layer.cross(partner.output_layer)
        child_network.layers[-1] = self.output_layer

        layer_counter = 1

        for i in range(1, len(self.layers) - 1):
            child_network.layers[-1 - layer_counter] = self.layers[-1 - layer_counter].cross(
                partner.layers[-1 - layer_counter]
            )

            child_network.layers[-1 - layer_counter].next_layer = self.layers[-layer_counter]

        child_network.input_layer = self.input_layer.cross(partner.input_layer)
        child_network.input_layer.next_layer = self.layers[1]
        child_network.layers[0] = self.input_layer

        return child_network

    def draw_network(self, SURFACE):
        '''Draw the neural network to a surface'''
        SURFACE.fill((0, 0, 0))

        width = SURFACE.get_width()
        height = SURFACE.get_height()

        n_layers = len(self.layers)
        space_between_layers = width / (n_layers + 1)

        largest_layer = self.input_layer.num_neurons
        for layer in self.layers:
            largest_layer = max(largest_layer, layer.num_neurons)

        neuron_radius = min(
            min(25, space_between_layers / 2),
            min(25, height / largest_layer - 2 * largest_layer)
        )

        # Position the nodes
        cur_layer_x = space_between_layers
        drawn_nodes = [] # tuple of x,y positions

        for i in range(n_layers):
            cur_layer_y = (height / 2) - (4*neuron_radius + 5) * (self.layers[i].num_neurons / 2)
            for j in range(self.layers[i].num_neurons):
                drawn_nodes.append((cur_layer_x, cur_layer_y))

                cur_layer_y += 4*neuron_radius
            cur_layer_x += space_between_layers

        # Draw weights between nodes
        cur_node = 0
        for i in range(n_layers):
            next_layer = cur_node + self.layers[i].num_neurons
            for j in range(self.layers[i].num_neurons):
                for k in range(len(self.layers[i].weights)):
                    # Draw weights from neuron j in layer i
                    
                    weight = self.layers[i].weights[k][j]
                    line_start = drawn_nodes[cur_node]
                    line_end = drawn_nodes[next_layer + k]

                    color = (0, 150, 0)
                    if weight < 0:
                        color = (150, 0, 0)

                    pygame.draw.line(SURFACE, color, line_start, line_end, round(abs(2 * weight)))

                cur_node += 1
        
        for i in range(len(drawn_nodes)):
            pos = drawn_nodes[i]
            pygame.draw.circle(SURFACE, (200, 200, 200), pos, neuron_radius)