from .activationFunctions import sigmoid
import random
random = random

# INNOVATION COUNTER
GlobalInnovationCounter = 0

#Activation function
activationFunctions = {
	'sigmoid': sigmoid
}
outputNodeActivation = 'sigmoid'
hiddenNodeActivation = 'sigmoid'

# NEAT parameters
noOfInputNodes = 2
noOfOutputNodes = 1
mutateStructure = True
populationSize = 100
totalGenerations = 500

# Speciation parameters
delta = 3.0
disjointAndExcessGeneFactor = 1
weightDifferenceFactor = 1

# Reproduction parameters
deletionFactor = 0.8
mutateAddConnection = 0.01
mutateAddNode = 0.01
mutateChangeWeight = 0.8
mutateEnableGene = 0.05
