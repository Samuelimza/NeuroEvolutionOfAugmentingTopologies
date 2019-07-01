import sys, os, random

# Make sure that the application source directory (this directory's parent) is
# on sys.path.

here = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, here)

import neat
from neat.genome import Genome

def fitnessFunc(neuralNetworks):
	fitness = []
	for nn in neuralNetworks:
		fitness.append(random.random() * 10)
	return fitness

neatHello = neat.Main.NEAT(fitnessFunc)
# genomesAfterTraining = neatHello.train()

genome = Genome()
for connectionKey in genome.connectionGenes.keys():
	print('Index : {}, Innov No.: {}'.format(connectionKey, genome.connectionGenes[connectionKey].innovationNumber))

#for genome in genomesAfterTraining:
#	genome.printDetails()

#neat.speciate.speciate(neatHello.population)

#myFuckingDict = {}
#for genome in neatHello.population.genomes:
#	if genome.species not in myFuckingDict.keys():
#		myFuckingDict[genome.species] = []
#	myFuckingDict[genome.species].append(genome)

#for specie in myFuckingDict:
#	print("########################")
#	print("Printing species: ", specie)
#	print("########################")
#	for genome in myFuckingDict[specie]:
#		genome.printDetails()
