import network_self
import car
import numpy as np

class Race(object):

	def __init__(self, parameters, environment):
		# Imports network and environment from evolve
		self.biases = parameters[0]
		self.weights = parameters[1]
		self.sizes = parameters[2]
		self.environment = environment
		# Performance metrics
		self.race_time = 0
		#self.average_speed = 0 # Going to be used later as a metric of success

	def race(self):
		''' Race simulates a race given a certain set of conditions: network(policy),
		car constants(metrics), and environment
		'''
		# Initializes a network self.mutated_network with the imported parameters
		self.mutated_network_initializer()
		
		# Initializes vehicle, including its position and time
		self.initialize_car()
		self.set_car_constants()

		stop = 0 # TEMP counter used to measure distance traveled rather than time taken
		while True:
			stop += 1

			# Prepare inputs to neural network
			self.get_nn_inputs()

			# Find output velocity from neural network
			velocity = self.mutated_network.feedforward_minus_last(self.inputs)

			if velocity == 0: #TEMP end race if network output is 0
				break

			# Update car state based on velocity
			self.car.update_state(velocity)

			#if velocity > 0:
				#print('velocity ', velocity, 'm/s')
				#print('racetime ', self.car.race_time/60, 'minutes')
				#print('distance ', self.car.position/1000, 'km')
				#print('charge   ', self.car.battery_charge/1000, 'kJ')
				#print()
				
			self.race_time = self.car.race_time
			if self.inputs[0] < 0: # end race if reached finish line
				break
			if stop == 10:	# TEMP end race after 10 time steps 
				break

	def mutated_network_initializer(self):
		# exports network parameters to network_self class
		self.mutated_network = network_self.Network( self.sizes )
		self.mutated_network.biases = self.biases
		self.mutated_network.weights = self.weights

	def get_nn_inputs(self):
		''' Produce a vector of inputs to neural network

		Data is changed to better fit between 0-1 for better nn input
		'''

		# distance from finish line information
		inverse_distance_to_finish = ((self.environment[0]-self.car.position/1e6)**-1)/10
		
		# battery state as a percentage
		battery_charge = self.car.battery_charge/self.car.max_charge
		
		# time of day - hours from solar hour (noon)
		time_hour = self.car.clock_time/6

		input_size = 3 #number of input neurons

		# input must be an np.array of shape (input_size, 1)
		self.inputs = np.zeros( (input_size,1) )
		self.inputs[0] = inverse_distance_to_finish
		self.inputs[1] = battery_charge
		self.inputs[2] = time_hour

	def initialize_car(self):
		# Starting racing conditions of the car
		self.car = car.Car(
			starting_position =0, 
			starting_time = 0, 
			starting_charge = 1.6e7, 
			panel_temperature = 25,
			time_step = 600, 
			clock_time = 0, 
			cell_voltage = 3.5
			)

	def set_car_constants(self):
		# Properties of the car
		self.car.set_constants(
			mass = 240,
			E_regen = 0.8, 
			max_charge = 1.6e7, 
			Cd = 0.12, 
			Crr = 0.03,
			Frontal_Area = 1, 
			solar_hour = -4, 
			panel_area = 6 , 
			basecell_efficiency = 0.16,
			battery_inefficiency = 0.00005
			)
