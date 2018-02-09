import network_self
import numpy as np
import evolve

# specify data input size, should be automated later using evolve method
input_size = 3

# specify desired network shape
net_shape = [input_size, 6, 1]

# initialize new random network/ option to import existing should be added
strategy = network_self.Network(net_shape)

# exports network to evolution class
evolve = evolve.Evolution(net_sizes = strategy.sizes, 
						net_biases = strategy.biases, 
						net_weights = strategy.weights)

# executes evolutionary model algorithm
evolve.evolve(population_size = 50, 
			mutation_rate = 0.1, 
			selection_bias = 1, 
			inheritance_rate = 2,
			generations = 20)
