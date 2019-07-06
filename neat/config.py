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
totalGenerations = 100

# Percentage of low scoring individuals to be deleted
deletionFactor = 0.3

# Mutation rates
mutateAddConnection = 0.1
mutateAddNode = 0.05
mutateChangeWeight = 0.7
mutateEnableGene = 0.05

# Structure of the starting neural network
noOfInputNodes = 2
noOfOutputNodes = 1

# Activation function usage
outputNodeActivation = 'sigmoid'
hiddenNodeActivation = 'sigmoid'

# Speciation parameters
delta = 3.0
