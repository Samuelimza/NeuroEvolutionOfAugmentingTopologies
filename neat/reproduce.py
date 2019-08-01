import math
from copy import deepcopy
from .genome import Genome
from . import config


def reproduce(population, speciesAsLists, fitness, reporter):
	newGenomes = []

	sumPerSpecies, totalFitness = adjustAndAssignFitness(population, speciesAsLists, fitness)
	reportSpeciesFitness(speciesAsLists, reporter)
	speciesSorted = sortSpecies(speciesAsLists)

	if reporter.generation % 30 == 0:
		for specie in reversed(speciesSorted):
			if determineSpecieAge(specie, reporter) >= 20:
				obliterate(specie, speciesAsLists)
				break

	obliterateStagnantSpecies(speciesAsLists, reporter)

	elite = Genome.createDuplicateChild(speciesAsLists[speciesSorted[0]][0])
	newGenomes.append(elite)

	offSpringCount = determineOffSpringCount(speciesAsLists, sumPerSpecies, totalFitness, reporter)

	connectionMutations = []
	nodeMutations = []

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
		genome.originalFitness = fitness[counter]
		genome.fitness = fitness[counter] / len(speciesAsLists[genome.species])
		if genome.species not in sumPerSpecies.keys():
			sumPerSpecies[genome.species] = 0
		sumPerSpecies[genome.species] += genome.fitness
		totalFitness += genome.fitness
		counter += 1
	return sumPerSpecies, totalFitness


def reportSpeciesFitness(speciesAsLists, reporter):
	dictionary = {}  # dictionary[generation][specie] == maxFitnessOfThatSpecieThatGeneration
	for specie in speciesAsLists:
		speciesAsLists[specie] = sorted(speciesAsLists[specie], key=lambda g: g.fitness, reverse=True)
		dictionary[specie] = speciesAsLists[specie][0].originalFitness  # (max(speciesAsLists[specie], key=lambda g: g.fitness)).fitness
	reporter.speciesWiseFitness.append(dictionary)


def sortSpecies(speciesAsLists):
	species = list(speciesAsLists.keys())
	species = sorted(species, key=lambda s: speciesAsLists[s][0].originalFitness, reverse=True)
	return species


def determineSpecieAge(specie, reporter):
	age = 0
	for aSingleGenSpecieWiseFitness in reversed(reporter.speciesWiseFitness):
		if specie in aSingleGenSpecieWiseFitness:
			age += 1
		else:
			return age
	return age


def obliterate(specie, speciesAsLists):
	# TODO: Report obliteration
	for genome in speciesAsLists[specie]:
		genome.fitness *= 0.01


def obliterateStagnantSpecies(speciesAsLists, reporter):
	for specie in speciesAsLists:
		stagnant = True
		lastImproved = reporter.generation - config.stagnantAge
		lastFitness = reporter.speciesWiseFitness[lastImproved][specie]
		for i in range(lastImproved, reporter.generation + 1):
			if reporter.speciesWiseFitness[i][specie] > lastFitness:
				stagnant = False
				break
		if stagnant:
			obliterate(specie, speciesAsLists)


def determineOffSpringCount(speciesAsLists, sumPerSpecies, totalFitness, reporter):
	offSpringCount = {}
	for specie in speciesAsLists:
		pass
	return offSpringCount


def select(genomes):
	return config.random.choice(genomes)
