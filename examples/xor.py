import os
import sys
# Make sure that the application source directory (this directory's parent) is on sys.path.
here = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, here)


import neat
import numpy as np


def fitnessFunc(neuralNetworks):
	fitness = []
	inputs = np.array([[0.0, 0.0],
					   [0.0, 1.0],
					   [1.0, 0.0],
					   [1.0, 1.0]]
					  )
	outputTrain = np.array([[0.0],
							[1.0],
							[1.0],
							[0.0]]
						   )

	for nn in neuralNetworks:
		outputNN = nn.activate(inputs)
		individualFitness = 4.0 - np.sum(np.square(outputNN - outputTrain))
		fitness.append(individualFitness)
		nn.genome.output = outputNN
	return fitness


neatHello = neat.Main.NEAT(fitnessFunc)
# for genome in neatHello.population.genomes:
#     genome.addNode(0, 2, 3)
#     genome.addNode(1, 4, 5)
#     genome.addConnection(1, 2, 1.0, True, 6)
#     genome.addConnection(0, 3, 1.0, True, 7)
#
#     genome.connectionGenes[2].weight = 20.0
#     genome.connectionGenes[6].weight = 20.0
#     genome.connectionGenes[3].weight = 20.0
#     genome.connectionGenes[5].weight = 20.0
#     genome.connectionGenes[7].weight = -20.0
#     genome.connectionGenes[4].weight = -20.0
#     genome.nodeGenes[2].bias = -10
#     genome.nodeGenes[-1].bias = -30
#     genome.nodeGenes[3].bias = 30
#
#     genome.printDetails()

genomesAfterTraining = neatHello.train()

for genome in genomesAfterTraining:
	# genome.printDetails()
	pass
