import sys, os

# Make sure that the application source directory (this directory's parent) is
# on sys.path.

here = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, here)

import neat
print(dir(neat))
neatHello = neat.Main.NEAT(2)

neat.speciate.speciate(neatHello.population)

myFuckingDict = {}
for genome in neatHello.population.genomes:
	if genome.species not in myFuckingDict.keys():
		myFuckingDict[genome.species] = []
	myFuckingDict[genome.species].append(genome)

for specie in myFuckingDict:
	print("########################")
	print("Printing species: ", specie)
	print("########################")
	for genome in myFuckingDict[specie]:
		genome.printDetails()
