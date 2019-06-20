import math

from neat.activationFunctions import sigmoid

# INNOVATION COUNTER
GlobalInnovationCounter = 0
# INNOVATION COUNTER

#Activation function setup
activationFunctions = {}
activationFunctions['sigmoid'] = sigmoid

config = {}

'''
NEAT parameters
'''
config['populationSize'] = 100

# Structure of the starting neural network
config['noOfInputNode'] = 2
config['noOfOutputNodes'] = 1

# Activation function usage
config['outputNodeActivation'] = 'sigmoid'
config['hiddenNodeActivation'] = 'sigmoid'
