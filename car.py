import numpy as np 
import random
from math import pi as pi
from math import sin as sin
from math import cos as cos
from math import acos

# Set up starting conditions
# add function to input velocity and return next car state after 60 seconds

class Car(object):

	def __init__(self, starting_position =0, starting_time = 0, starting_charge = 0, 
		battery_temperature = 25, panel_temperature = 25, time_step = 600, 
		clock_time = 0, cell_voltage = 3.5):
		# states
		self.position = starting_position
		self.race_time = starting_time
		self.clock_time = clock_time #time to solar hour
		self.battery_charge = starting_charge
		self.time_step = time_step
		self.pack_voltage = 28*cell_voltage
		# properties

	def set_constants(self, mass, E_regen, max_charge, Cd, Crr,
					Frontal_Area, solar_hour, panel_area, basecell_efficiency,
					battery_inefficiency):
		#Car Constants
		self.mass = mass
		#Battery Constants
		self.E_regen = E_regen
		self.power_inefficiency = battery_inefficiency 
		self.max_charge = max_charge
		#Motion Constants
		self.Cd = Cd
		self.Crr = Crr
		self.Frontal_Area = Frontal_Area
		#Location Constants
		self.solar_hour = solar_hour
		#Panel Constants
		self.panel_area = panel_area
		self.basecell_efficiency = basecell_efficiency
		self.irradiance()

	def update_state(self, velocity):
		self.position += self.time_step * velocity
		self.race_time += self.time_step
		self.clock_time += self.time_step/3600
		self.update_battery_charge(velocity)
		return 

	def update_battery_charge(self, velocity):
		# net_power is solar power into panels
		net_power = self.irradiance()* self.basecell_efficiency * self.panel_area
		self.sensor_solar_p = net_power
		# net_power is the net power TO batteries (not in batteries)
		net_power -= self.motion_loss(velocity)
		# heat loss due to current
		self.sensor_battery_heat_loss = (self.power_inefficiency) * net_power**2

		# if net power is positive, battery takes in less power than net_power
		if net_power > 0:
			self.sensor_battery_dCharge = net_power - self.sensor_battery_heat_loss
			self.battery_charge += self.sensor_battery_dCharge * self.time_step
		# if net power is negative, battery drains more power than net_power
		else:
			self.sensor_battery_dCharge = net_power - self.sensor_battery_heat_loss
			self.battery_charge += self.sensor_battery_dCharge * self.time_step

		self.sensor_avg_battery_current = -self.sensor_battery_dCharge/ self.pack_voltage
	
	def irradiance(self):
		self.sensor_solar_p = 1000 * cos(self.solar_hour*pi/12)**1.5
		return self.sensor_solar_p

	def motion_loss(self, velocity):
		self.Aero_loss = velocity**3 * 0.5 * 1.225 * self.Frontal_Area * self.Cd

		#Rolling
		self.Rolling_loss = self.mass * 9.81 * self.Crr * velocity
		self.sensor_motion_p_loss = self.Aero_loss + self.Rolling_loss
		return self.sensor_motion_p_loss
