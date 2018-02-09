import numpy as np 
import random
from math import pi as pi
from math import sin as sin
from math import cos as cos
from math import acos

''' Contains functions modeling the physical behavior of the car

Purpose is to return the new car state (position/battery power) 
given a velocity, timestep, and environment

'''

class Car(object):

	def __init__(self, starting_position =0, starting_time = 0, starting_charge = 0, 
		battery_temperature = 25, panel_temperature = 25, time_step = 600, 
		clock_time = 0, cell_voltage = 3.5):
		
		# states
		self.position = starting_position # distance from start of race (meters)
		self.race_time = starting_time # time since start of race (seconds)
		self.clock_time = clock_time # time to solar hour
		self.battery_charge = starting_charge # charge at start of race
		self.time_step = time_step # time spent at a velocity
		self.pack_voltage = 28*cell_voltage # TEMP voltage of battery pack


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
		self.Cd = Cd # coefficient of drag
		self.Crr = Crr # coefficient of rolling resistance
		self.Frontal_Area = Frontal_Area
		#Location Constants
		self.solar_hour = solar_hour # (need to fix redundancy) also time to solar hour
		#Panel Constants
		self.panel_area = panel_area # available panel area
		self.basecell_efficiency = basecell_efficiency # solar cell efficiency
		self.irradiance()

	def update_state(self, velocity):
		self.position += self.time_step * velocity # update position (meters)
		self.race_time += self.time_step # update time since start of race (seconds)
		self.clock_time += self.time_step/3600 # update clock time (hours)
		self.update_battery_charge(velocity) # update battery charge
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
		# find solar power incident to solar array (not absorbed)
		self.sensor_solar_p = 1000 * cos(self.solar_hour*pi/12)**1.5
		return self.sensor_solar_p

	def motion_loss(self, velocity):
		# power loss due to aerodynamics
		self.Aero_loss = velocity**3 * 0.5 * 1.225 * self.Frontal_Area * self.Cd

		# power loss due to rolling resistance
		self.Rolling_loss = self.mass * 9.81 * self.Crr * velocity
		
		self.sensor_motion_p_loss = self.Aero_loss + self.Rolling_loss
		return self.sensor_motion_p_loss
