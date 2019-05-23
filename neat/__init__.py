import math

from activationFunctions import sigmoid

activationFunctions = {}
activationFunctions['sigmoid'] = sigmoid

config = {}

# Structure of the starting neural network
config['noOfInputNode'] = 2
config['noOfOutputNodes'] = 1

# Activation function usage
config['outputNodeActivation'] = 'sigmoid'
config['hiddenNodeActivation'] = 'sigmoid'
