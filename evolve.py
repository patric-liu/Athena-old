import numpy as np
import network_self


class Evolution(object):

	def __init__(self, net_sizes, net_biases, net_weights):
		# import network
		self.sizes = net_sizes #list of sizes
		self.biases = net_biases
		self.weights = net_weights
		self.parameters = [self.biases, self.weights]

	def evolve(self, population_size, mutation_rate, selection_bias, inheritance_rate):
		# Returns slightly improved network
		'''Create multiple random versions of network'''
		self.clone(population_size, mutation_rate)
		'''	Keep track of their differences from original

		run each through the same training map
			input network, return total time'''
		self.determine_fitness()
		'''Find the difference between time and mean_time for all networks
			raise the difference to the power of 1+selection_bias'''
		self.reproduce(selection_bias, inheritance_rate)
		'''Multiply deltas by time_difference^(1+selection_bias) to create new network'''

	def clone(self, population_size, mutation_rate):
		# prepare list of deltas and population parameters
		self.mutations = []
		self.clones = []
		for n in range(population_size):
			# randomly generate mutations
			bias_mutation  = [np.random.randn(y, 1) for y in self.sizes[1:]]
			weight_mutation = [np.random.randn(y, x)/np.sqrt(x) 
						for x, y in zip(self.sizes[:-1], self.sizes[1:])]
			mutation = [bias_mutation, weight_mutation]
			self.mutations.append(mutation)
			# apply mutations to parent network
			clone_biases = [x * mutation_rate + y for x,y 
						in zip(bias_mutation, self.biases)]
			clone_weights = [x * mutation_rate + y for x,y 
						in zip(weight_mutation, self.weights)]
			clone_parameters = [new_biases, new_weights]
			self.clones.append(clone_parameters)

	def determine_fitness(self):
		self.times = []
		# return race time (fitness)
		'''initialize map and information
		race
		For each network:
			initializes network
			While racing:
				Feedforward
				simulate
				update information
				end when race is done
			save time taken'''
		# initialize map
		race_times = []
		for n in range(population_size):
			#initialize network
			self.mutated_network_initializer()
			mutated_network = network_self.Network( self.sizes )
			mutated_network.biases = self.clones[n][0]
			mutated_network.weights = self.clones[n][1]
			#initialize car
			self.car_initializer()
			Racing = True
			while Racing:
				Velocity = feedforward(inputs)
				car.update_state(velocity)
				update(info)
				if distance_to_finish < 0:
					Racing = False
			race_times.append(car.race_times)


		#return times
	def reproduce(self, selection_bias, inheritance_rate):
		# return relative performance

		mean_speed = np.sum(self.times)/population_size
		weight = [(time-mean_speed)**selection_bias * inheritance_rate
					 for time in self.times]

		# new parameters formed by adding the weighted 
		# sum of mutations to parent network
		mutation_vector = [w*m for w,m in zip(weight, self.mutations)]
		self.new_parameters = self.parameters + mutation_vector
