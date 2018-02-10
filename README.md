# Athena
Athena is a neural network that determines race strategy for week-long, 3000 km solar vehicle races. It's trained in simulation using evolutionary methods and validated in real physical testing. Once trained, Athena can quickly run during the race and respond to changing weather conditions and unexpected deviations from the proposed strategy.

The evolutionary method used works by creating multiple slightly tweaked versions of Athena, and allows them to determine strategy for a simulated race. At the end of the simulations, Athena is updated based on the performance of each version. This is then repeated, along with real testing, until Athena suprasses our team member's abilities to make strategic decisions. 

This evolutionary approach relies on accurate yet efficient simulations of relevant physical systems, dynamics randomization, generated race maps, and reading of real weather data. The next step for this project would be to explore the use of reinforcement learning methods in this system of massively delayed rewards. 

## Docs


trainer.py - Training interface that allows you to specify training hyperparameters

evolve.py - Implements the evolution algorithm

race.py - Runs athena through a simulation

car.py - Contains functions which model the physical behavior of the car

network_self.py - Contains neural network functionality

###future functionality

generate_environment.py - Generates a random race map 

read_weather_data.py - Reads live NOAA data for 

interpret_weather.py - Applies 1-d convolution and pooling to high-dimensional weather and map data to extract lower dimensional features to input to the neural network

run_Athena -  runs Athena, pulling data from live telemetry feed, weather forecasts and if needed, human input

Athenas/ - Holds all saved versions of Athena


## Aside


Solar vehicle racing is at its core, a challenge of vehicle energy efficiency and energy management. When building a solar vehicle, vast amounts of time are rightfully spent on design, manufacturing, and testing for reliability - the building of the car. However once at the race, much of this effort can be quickly negated if race strategy is conducted poorly. Hopefully, Athena can support my team during the race and allow the vehicle that everyone spent so long desinging and building to perform to the best of its ability. 
