import math
from .genome import Genome
from . import config


def reproduce(population, speciesAsLists, fitness, reporter):
	newGenomes = []

	adjustAndAssignFitness(population, speciesAsLists, fitness)
	reportSpeciesFitness(speciesAsLists, reporter)
	speciesSorted = sortSpecies(speciesAsLists)

	if reporter.generation % 30 == 0:
		for specie in reversed(speciesSorted):
			if determineSpecieAge(specie, reporter) >= 20:
				obliterate(specie, speciesAsLists, reporter)
				break

	if reporter.generation > 15:
		obliterateStagnantSpecies(speciesAsLists, reporter)
	reporter.maxFitness.append(speciesAsLists[speciesSorted[0]][0].originalFitness)
	elite = speciesAsLists[speciesSorted[0]][0].createDuplicateChild()
	newGenomes.append(elite)
	offSpringCount = determineOffSpringCount(speciesAsLists, reporter)

	connectionMutations = []
	nodeMutations = []

	for specie in speciesAsLists:
		if offSpringCount[specie] <= 0:
			reporter.extinctSpecies.append(specie)
			# TODO: Remove specie representative from representatives?
			continue
		offspringFromMating = math.floor(config.matingQuota * offSpringCount[specie])
		offspringFromMutation = math.ceil(config.mutateQuota * offSpringCount[specie])
		genomesDeleted = math.ceil(config.survivalThreshold * len(speciesAsLists[specie]))
		# del speciesAsLists[specie][genomesDeleted:]
		try:
			for i in range(offspringFromMutation):
				newGenome = config.random.choice(speciesAsLists[specie][0:genomesDeleted]).createDuplicateChild()
				newGenome.mutate(connectionMutations, nodeMutations)
				newGenomes.append(newGenome)
			for i in range(offspringFromMating):
				newGenome = Genome.crossover(config.random.choice(speciesAsLists[specie][0:genomesDeleted]), config.random.choice(speciesAsLists[specie][0:genomesDeleted]))
				newGenome.mutate(connectionMutations, nodeMutations)
				newGenomes.append(newGenome)
		except IndexError:
			pass
	stolenBabies = config.populationSize - len(newGenomes)
	for i in range(stolenBabies):
		if len(speciesSorted) > 1:
			if i < math.ceil(stolenBabies / 2):
				newGenome = speciesAsLists[speciesSorted[0]][0].createDuplicateChild()
				newGenome.mutate(connectionMutations, nodeMutations)
				newGenomes.append(newGenome)
			else:
				newGenome = speciesAsLists[speciesSorted[1]][0].createDuplicateChild()
				newGenome.mutate(connectionMutations, nodeMutations)
				newGenomes.append(newGenome)

	reporter.stolenBabies = stolenBabies
	reporter.speciesSorted = speciesSorted
	population.genomes = newGenomes


def adjustAndAssignFitness(population, speciesAsLists, fitness):
	# Adjust fitness with fitness sharing
	counter = 0
	for genome in population.genomes:
		genome.originalFitness = fitness[counter]
		genome.originalCounter = counter
		genome.fitness = fitness[counter] / len(speciesAsLists[genome.species])
		counter += 1


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


def obliterate(specie, speciesAsLists, reporter):
	reporter.obliteratedSpecies.append(specie)
	for genome in speciesAsLists[specie]:
		genome.fitness *= 0.01


def obliterateStagnantSpecies(speciesAsLists, reporter):
	try:
		for specie in speciesAsLists:
			stagnant = True
			lastImproved = reporter.generation - config.stagnantAge
			if specie not in reporter.speciesWiseFitness[lastImproved]:
				continue
			lastFitness = reporter.speciesWiseFitness[lastImproved][specie]
			for i in range(lastImproved, reporter.generation + 1):
				if reporter.speciesWiseFitness[i][specie] > lastFitness:
					stagnant = False
					break
			if stagnant:
				obliterate(specie, speciesAsLists, reporter)
	except KeyError:
		pass


def determineOffSpringCount(speciesAsLists, reporter):
	offSpringCount = {}
	sumPerSpecies = {}
	totalFitness = 0
	for specie in speciesAsLists:
		sumPerSpecies[specie] = sum(genome.fitness for genome in speciesAsLists[specie])
		totalFitness += sumPerSpecies[specie]
	for specie in speciesAsLists:
		offSpringCount[specie] = math.floor(config.populationSize * sumPerSpecies[specie] / totalFitness)
	return offSpringCount

