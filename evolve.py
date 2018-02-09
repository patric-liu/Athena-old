import numpy as np
import race

''' Uses Evolutionary Models to improve network

Creates multiple versions ('clones') of original network with slight 
pertubations ('mutations') to the parameters, runs them through a race 
simulation, and creates a new network ('child') using a weighted 
average of each clone based on its performance ('fitness')

Child then becomes the original network and this is looped over 'generations'

'''

class Evolution(object):

	def __init__(self, net_sizes, net_biases, net_weights):
		# import network from trainer
		self.sizes = net_sizes #list of sizes
		self.biases = net_biases
		self.weights = net_weights
		self.parameters = [self.biases, self.weights, self.sizes]

	def evolve(self, population_size, mutation_rate, selection_bias, inheritance_rate, generations):
		''' Evolve
		Main training method, taking original network (self.parameters) and replaces
		it with an evolved one
		
		population_size: number of clones to make/evaluate each generation
		
		mutation_rate: amount by which the clones vary from the parent
		
		selection_bias: how strongly the weights favor better performance
		
		inheritance_rate: amount by which the child varies from the parent
		
		generations: number of generations to evolve over


		'''
		for generation in range(generations):

			# creates clones of original network
			self.clone_parent(population_size, mutation_rate)
			# runs clones through the simulatin to determine fitness
			self.determine_fitness(population_size)
			# creates child network using clones based on fitness
			self.reproduce(selection_bias, inheritance_rate, population_size)

	def clone_parent(self, population_size, mutation_rate):
		self.mutations = []
		self.clones = []
		for n in range(population_size):
			# randomly generate mutations
			bias_mutation  = [np.random.randn(y, 1) for y in self.sizes[1:]]
			weight_mutation = [np.random.randn(y, x)/np.sqrt(x) 
						for x, y in zip(self.sizes[:-1], self.sizes[1:])]
			mutation = [bias_mutation, weight_mutation]
			self.mutations.append(mutation)

			# apply mutations to parent network to create clones
			clone_biases = [x * mutation_rate + y for x,y 
						in zip(bias_mutation, self.biases)]
			clone_weights = [x * mutation_rate + y for x,y 
						in zip(weight_mutation, self.weights)]
			clone_parameters = [clone_biases, clone_weights, self.sizes]
			self.clones.append(clone_parameters)

	def determine_fitness(self, population_size):
		self.times = []				# time or distance is used as a fitness metric for testing purposes, time will be used for final product
		self.distances = []			# distance is currently being used for testing
		self.environment = [100000] # **temporary replacement for a real environment **
		
		# runs each clone through simulation to determine its fitness
		for n in range(population_size): 

			# export clone's network parameters and environment to set up a race
			competition = race.Race(self.clones[n], self.environment)

			# runs through a race allowing clone to determine strategy
			competition.race()


			self.distances.append(competition.car.position/1000) # testing: saves the distance traveled
		self.times = self.distances # temporary convenience measure for testing purposes

		#print()
		#print(self.distances)
		#print('generation average distance: ', np.sum(self.distances)/population_size)

	def reproduce(self, selection_bias, inheritance_rate, population_size):
			''' Reproduce - creates a child network based on clone performance
			A new mutation equal to the weighted average of ckone mutations 
			is applied to the original network. Weights are proportional 
			to (clone performance[i] - average clone performance)^selection_bias
			Inheritance rate scales how big the new mutation is. 

			'''

			# Create list of weights
			mean_speed = np.sum(self.times)/population_size
			weights = [(time-mean_speed)**selection_bias * inheritance_rate
					 for time in self.times]

			# Initialize child network
			child_net = self.parameters[:]
			# Loop through the numpy arrays that make up the parameters
			for parameter_type in [0,1]: # No 2 index to preserve self.sizes
				for index in range(len(self.sizes)-1):

					# Initialize np array from 1st clone **required to properly sum**
					parameter_deltas = self.mutations[0][parameter_type][index] * weights[0] * inheritance_rate

					# Add weighted np arrays from rest of clones,
					for clone in range(1, population_size):
						parameter_deltas = parameter_deltas + self.mutations[clone][parameter_type][index] * weights[clone] * inheritance_rate
					
					# Normalize parameter changes by population size and update child_net
					parameter_deltas = parameter_deltas / float(population_size)
					child_net[parameter_type][index] = child_net[parameter_type][index] + parameter_deltas



			# Determien and display performance of child network
			competition = race.Race(child_net, self.environment)
			competition.race()
			print('new gen: ', competition.car.position/1000)

