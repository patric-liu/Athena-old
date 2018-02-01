import car

###############
# INPUTS HERE #
###############

solar_hour = 0 # hours from noon (Noon is directly above)
velocity = 25 # velocity input, m/s

time_step = 1  # seconds
cell_voltage = 3.5 # volts
Frontal_Area = 1 # meters^2
solar_cell_efficiency = 0.16 # cell Efficinecy
battery_infefficiency_constant = 0.00005 # unitless, multiplied by square of battery power draw to get power loss

###############
###############

car = car.Car(starting_position =0, starting_time = 0, starting_charge = 0, 
				panel_temperature = 25, time_step = time_step, 
				clock_time = 0, cell_voltage = cell_voltage)

car.set_constants(mass = 240, E_regen = 0.8, max_charge = 1.6e7, Cd = 0.12, Crr = 0.03,
					Frontal_Area = Frontal_Area, solar_hour = solar_hour, panel_area = 6 , 
					basecell_efficiency = solar_cell_efficiency,
					battery_inefficiency = battery_infefficiency_constant)

print(velocity*3.6, 'km/h')
car.update_state(velocity)
#"{:.2f}".format(
print("{:.2f}".format(car.position), 'meters')
print("{:.2f}".format(car.race_time), 'seconds')
print("{:.2f}".format(car.battery_charge/1000), 'Megajoules charge in battery')
print("{:.2f}".format(car.sensor_battery_dCharge * car.time_step), 'change in charge this timestep')
print()
print("{:.2f}".format(car.sensor_solar_p), 'Watts power in from cells')
print("{:.2f}".format(car.sensor_motion_p_loss), 'Watts power loss from motion')
print("{:.2f}".format(car.sensor_battery_heat_loss), 'Watts heat waste in batteries')
print("{:.2f}".format(car.sensor_battery_dCharge), 'Watts change in charge')
print()
print("{:.2f}".format(car.Aero_loss),'Aero Power Loss ', )
print("{:.2f}".format(car.Rolling_loss),'Rolling Power Loss ')
print("{:.2f}".format(car.sensor_avg_battery_current), 'Amp current draw')

