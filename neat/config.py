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
populationSize = 150
totalGenerations = 300

# Speciation parameters
delta = 3.0
disjointAndExcessGeneFactor = 1
weightDifferenceFactor = 0.4

# Reproduction parameters
survivalThreshold = 0.2
matingQuota = 0.6
mutateQuota = 0.4
mutateStructureProb = 0.5
mutateAddConnection = 0.07
mutateAddNode = 0.03
mutateWeights = 0.8
perturbationProbability = 0.9
mutateEnableGene = 0.05
stagnantAge = 15
