import math

def reproduce(population, speciesAsLists, fitness):
	nextGenDistribution = {}
	sumPerSpecies = {}
	
	counter = 0
	for genome in population.genomes:
		fitness[counter] = fitness[counter] / len(speciesAsLists[genome.species])
		genome.fitness = fitness[counter]
		if genome.species not in sumPerSpecies.keys():
			sumPerSpecies[genome.species] = 0
		sumPerSpecies[genome.species] += fitness[counter]
		totalFitness += fitness[counter]
		counter += 1
	
	counter = 0
	newGenomes = []
	for specie in speciesAsLists.keys():
		offspringCount = math.ceil(len(population.genomes) * sumPerSpecies[specie] / totalFitness)
		for i in range(nextGenDistribution[specie]):
			newGenomes[counter] = crossover(select(spciesAsLists[specie]), select(spciesAsLists[specie]))
	
	population.genomes = newGenomes

def select(genomes):
	return random.select(genomes)
