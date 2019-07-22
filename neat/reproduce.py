import math, random
from .genome import Genome
from . import config


def reproduce(population, speciesAsLists, fitness):
	# Very confusing piece requires excessive commenting
	sumPerSpecies = {}
	totalFitness = 0

	# Debug
	# for specie in speciesAsLists:
	#	print('Species: {}, Length: {}'.format(specie, len(speciesAsLists[specie])))
	# Debug

	counter = 0
	for genome in population.genomes:
		# Adjust fitness based fitness sharing
		fitness[counter] = fitness[counter] / len(speciesAsLists[genome.species])
		genome.fitness = fitness[counter]
		# Calculate fitness sum of all individuals in a species
		if genome.species not in sumPerSpecies.keys():
			sumPerSpecies[genome.species] = 0
		sumPerSpecies[genome.species] += fitness[counter]
		# Also simultaneously increase total fitness of all individuals combined
		totalFitness += fitness[counter]
		counter += 1

	# TODO: Add features such as elitism etc.

	newGenomes = []
	connectionMutations = []
	nodeMutations = []
	for specie in speciesAsLists.keys():
		# Sort genomes of a specie based on their fitness
		sorted(speciesAsLists[specie], key=lambda genomeE: genomeE.fitness, reverse=True)
		# Calculate number of low fitness genomes to be deleted
		genomesDeleted = math.ceil((1 - config.deletionFactor) * len(speciesAsLists[specie]))
		# Delete low fitness genomes
		del speciesAsLists[specie][genomesDeleted:]
		# Calculate number of offsprings for next generation for a specie
		offspringCount = math.ceil(config.populationSize * sumPerSpecies[specie] / totalFitness)
		# Actually create offsprings
		for i in range(offspringCount):
			newGenome = Genome.crossover(select(speciesAsLists[specie]), select(speciesAsLists[specie]))
			newGenome.mutate(connectionMutations, nodeMutations)
			newGenomes.append(newGenome)
	population.genomes = newGenomes


def select(genomes):
	return random.choice(genomes)
