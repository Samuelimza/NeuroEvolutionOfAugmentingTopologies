# INNOVATION COUNTER
GlobalInnovationCounter = 0

#Activation function setup
activationFunctions = {}

from .activationFunctions import sigmoid
activationFunctions['sigmoid'] = sigmoid
'''
NEAT parameters
'''
populationSize = 100

# Structure of the starting neural network
noOfInputNodes = 4
noOfOutputNodes = 2

# Activation function usage
outputNodeActivation = 'sigmoid'
hiddenNodeActivation = 'sigmoid'

# Speciation parameters
delta = 0.5
