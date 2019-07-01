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

# Percenntage of low scorings individuals to be deleted
deletionFactor = 0.3

# Mutation rates
mutateAddConnection = 0.5
mutateAddNode = 0.5
mutateChangeWeight = 0.5
mutateEnableGene = 0.5

# Structure of the starting neural network
noOfInputNodes = 4
noOfOutputNodes = 2

# Activation function usage
outputNodeActivation = 'sigmoid'
hiddenNodeActivation = 'sigmoid'

# Speciation parameters
delta = 0.5
