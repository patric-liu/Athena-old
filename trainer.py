import network_self
import numpy as np
#import evolve
# Choose to create new network or upload existing
# Create New Network Class with random weights, just needs the ability to feedforward
# Input Size???
input_size = 2
# initialize random network
net_shape = [input_size, 1, 2, 3, 6, 7, 1]
strategy = network_self.Network(net_shape)
# initialize input vector
x = np.zeros( (input_size,1) )
# find output
y = strategy.feedforward_minus_last(x)
print(y)

#Give evolve network shape and parameters, it will return a better parametres one



# Loops through N generations
# 	Randomizes weights, with M Variations
# 	Loops through Simulation Steps
#		Feed Input > Feedforward2Vector > Add Noise to Vector
#		Update Car State
# 	Adjusts weights