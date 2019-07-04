import os
import sys

# Make sure that the application source directory (this directory's parent) is
# on sys.path.

here = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, here)

import neat


def fitnessFunc(neuralNetworks):
    fitness = []
    inputs = [[0.0, 0.0], [0.0, 1.0], [1.0, 0.0], [1.0, 1.0]]
    outputs = [0.0, 1.0, 1.0, 0.0]
    for nn in neuralNetworks:
        individualFitness = 4.0
        for i in range(len(inputs)):
            output = nn.activate(inputs[i])
            individualFitness -= (output[0] - outputs[i]) ** 2
        print('\t\t\tFitness: ', individualFitness)
        fitness.append(individualFitness)
    return fitness


neatHello = neat.Main.NEAT(fitnessFunc)
genomesAfterTraining = neatHello.train()

# genome = Genome()
# for connectionKey in genome.connectionGenes.keys():
#	print('Index : {}, Innov No.: {}'.format(connectionKey, genome.connectionGenes[connectionKey].innovationNumber))

for genome in genomesAfterTraining:
    genome.printDetails()

# neat.speciate.speciate(neatHello.population)

# myFuckingDict = {}
# for genome in neatHello.population.genomes:
#	if genome.species not in myFuckingDict.keys():
#		myFuckingDict[genome.species] = []
#	myFuckingDict[genome.species].append(genome)

# for specie in myFuckingDict:
#	print("########################")
#	print("Printing species: ", specie)
#	print("########################")
#	for genome in myFuckingDict[specie]:
#		genome.printDetails()
