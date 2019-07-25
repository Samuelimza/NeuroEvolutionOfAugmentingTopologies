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
totalGenerations = 500

# Percentage of low scoring individuals to be deleted
deletionFactor = 0.8

# Mutation rates
mutateAddConnection = 0.01
mutateAddNode = 0.01
mutateChangeWeight = 0.8
mutateEnableGene = 0.05

# Structure of the starting neural network
noOfInputNodes = 2
noOfOutputNodes = 1
mutateStructure = True

# Activation function usage
outputNodeActivation = 'sigmoid'
hiddenNodeActivation = 'sigmoid'

# Speciation parameters
delta = 3.0
