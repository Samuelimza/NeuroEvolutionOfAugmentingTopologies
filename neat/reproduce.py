import math
from copy import deepcopy
from .genome import Genome
from . import config


def reproduce(population, speciesAsLists, fitness, reporter):
	sumPerSpecies, totalFitness = adjustAndAssignFitness(population, speciesAsLists, fitness)
	reportSpeciesFitness(speciesAsLists, reporter)
	offSpringCount = determineOffSpringCount(speciesAsLists, sumPerSpecies, totalFitness, reporter)

	newGenomes = []
	connectionMutations = []
	nodeMutations = []

	maxFitness = max(fitness) # max(population.genomes, key = lambda g : g.fitness)
	eliteIndex = fitness.index(maxFitness)
	elite = deepcopy(population.genomes[eliteIndex])
	newGenomes.append(elite)

	for specie in speciesAsLists:
		offspringFromMating = math.ceil(config.populationSize * config.matingQuota * sumPerSpecies[specie] / totalFitness)
		offspringFromMutation = math.ceil(config.populationSize * config.mutateQuota * sumPerSpecies[specie] / totalFitness)
		# speciesAsLists[specie] = sorted(speciesAsLists[specie], key=lambda genomeE: genomeE.fitness, reverse=True)
		genomesDeleted = math.ceil((1 - config.deletionFactor) * len(speciesAsLists[specie]))
		del speciesAsLists[specie][genomesDeleted:]
		if offspringFromMating + offspringFromMutation <= 0:
			# TODO: (FEATURE) Report extinction
			continue
		for i in range(offspringFromMutation):
			newGenome = deepcopy(select(speciesAsLists[specie]))
			newGenome.species = None
			newGenome.mutate(connectionMutations, nodeMutations)
			newGenomes.append(newGenome)
		for i in range(offspringFromMating):
			newGenome = Genome.crossover(select(speciesAsLists[specie]), select(speciesAsLists[specie]))
			newGenome.mutate(connectionMutations, nodeMutations)
			newGenomes.append(newGenome)
	population.genomes = newGenomes


def adjustAndAssignFitness(population, speciesAsLists, fitness):
	sumPerSpecies = {}
	totalFitness = 0
	# Adjust fitness with fitness sharing and calculate sumPerSpecies and totalFitness
	counter = 0
	for genome in population.genomes:
		genome.fitness = fitness[counter] / len(speciesAsLists[genome.species])
		if genome.species not in sumPerSpecies.keys():
			sumPerSpecies[genome.species] = 0
		sumPerSpecies[genome.species] += genome.fitness
		totalFitness += genome.fitness
		counter += 1
	return sumPerSpecies, totalFitness


def reportSpeciesFitness(speciesAsLists, reporter):
	dictionary = {} # dictionary[generation][specie] == maxFitnessOfThatSpecieThatGeneration
	for specie in speciesAsLists:
		speciesAsLists[specie] = sorted(speciesAsLists[specie], key=lambda g: g.fitness, reverse=True)
		dictionary[specie] = speciesAsLists[specie][0]  # (max(speciesAsLists[specie], key=lambda g: g.fitness)).fitness
	reporter.speciesWiseFitness.append(dictionary)


def determineStagnantSpecies(speciesAsLists, sumPerSpecies, totalFitness, reporter):
	stagnantSpecies = []
	for specie in speciesAsLists:
		fitnessHistory = []
		for i in range(reporter.generation, reporter.generation - config.stagnantAge, -1):
			fitnessHistory.append(reporter.speciesWiseFitness[reporter.generations][specie])


def determineOffSpringCount(speciesAsLists, sumPerSpecies, totalFitness, reporter):
	offSpringCount = {}
	for specie in speciesAsLists:
		pass
	return offSpringCount


def select(genomes):
	return config.random.choice(genomes)
