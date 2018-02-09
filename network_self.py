import random
import numpy as np 

''' Neural Network

feedforward(input):
Returns the neural network output given its parameters and a certain input

feedforward_minus_list(input):
Returns the weighted inputs into the final layer of the neural network

weight_initializer():
Randomly generates parameters for a new network

'''

class Network(object):

	def __init__(self, sizes):			
		# Initializes the Characteristics of the Network

		# defines network shape: a list with the sizes of each layer in order
		self.sizes = sizes
		# number of network layers, including input and output layer
		self.num_layers = len(sizes)

		self.weight_initializer()

	def weight_initializer(self):
		""" Initializes weights and biases randomly
		Initializes with a normal distrubtuion, scaled such that the weighted inputs 
		to the next layer has a standard deviation of 2 and therefore avoids the
		learning slowdown cause by the slope of the sigmoid function at abs(z) >> 1
		"""
		self.biases  = [np.random.randn(y, 1) for y in self.sizes[1:]]

		self.weights = [np.random.randn(y, x)/np.sqrt(x) 
						for x, y in zip(self.sizes[:-1], self.sizes[1:])]

	def feedforward(self, a): 			
		# Return the output of the network for input 'a'
		for b, w in zip( self.biases,self.weights ):
			a = sigmoid(np.array(np.dot(w, a)) + b)
		return a

	def feedforward_minus_last(self, a): 			
		# Return the output of the network for input 'a'
		for n in range(self.num_layers-2):
			b = self.biases[n]
			w = self.weights[n]
			a = sigmoid(np.dot(w, a) + b)
		b = self.biases[self.num_layers-2]
		w = self.weights[self.num_layers-2]
		z = relu(np.dot(w, a) + b)
		return z

# element-wise sigmoid activation function
def sigmoid(z):						
	return 1.0/(1.0+np.exp(-z))

def relu(z):
	if z > 0:
		return z[0][0]
	else:
		return 0