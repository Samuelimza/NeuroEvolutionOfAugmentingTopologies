# INNOVATION COUNTER
GlobalInnovationCounter = 0

#Activation function setup
activationFunctions = {}

from .activationFunctions import sigmoid
activationFunctions['sigmoid'] = sigmoid
'''
NEAT parameters
'''
populationSize = 2
totalGenerations = 50

# Percenntage of low scorings individuals to be deleted
deletionFactor = 0.3

# Mutation rates
mutateAddConnection = 0.1
mutateAddNode = 0.1
mutateChangeWeight = 0.1
mutateEnableGene = 0.1

# Structure of the starting neural network
noOfInputNodes = 2
noOfOutputNodes = 1

# Activation function usage
outputNodeActivation = 'sigmoid'
hiddenNodeActivation = 'sigmoid'

# Speciation parameters
delta = 3.0
