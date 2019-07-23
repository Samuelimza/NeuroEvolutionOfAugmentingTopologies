# INNOVATION COUNTER
GlobalInnovationCounter = 0

#Activation function setup
activationFunctions = {}

from .activationFunctions import sigmoid
activationFunctions['sigmoid'] = sigmoid
'''
NEAT parameters
'''
populationSize = 50
totalGenerations = 1000

# Percentage of low scoring individuals to be deleted
deletionFactor = 0.8

# Mutation rates
mutateAddConnection = 0.005
mutateAddNode = 0.005
mutateChangeWeight = 0.8
mutateEnableGene = 0.05

# Structure of the starting neural network
noOfInputNodes = 2
noOfOutputNodes = 1
mutateStructure = False

# Activation function usage
outputNodeActivation = 'sigmoid'
hiddenNodeActivation = 'sigmoid'

# Speciation parameters
delta = 3.0
