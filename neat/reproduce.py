import math

def reproduce(population, speciesAsLists, fitness):
	nextGenDistribution = {}
	sumPerSpecies = {}
	
	counter = 0
	for genome in population.genomes:
		fitness[counter] = fitness[counter] / len(speciesAsLists[genome.species])
		if genome.species not in sumPerSpecies.keys():
			sumPerSpecies[genome.species] = 0
		sumPerSpecies[genome.species] += fitness[counter]
		totalFitness += fitness[counter]
		counter += 1
		
	for specie in sumPerSpecies.keys():
		nextGenDistribution[specie] = math.ceil(len(population.genomes) * sumPerSpecies[specie] / totalFitness)
	
	counter = 0
	newGenomes = []
	for specie in speciesAsLists.keys():
		for i in range(nextGenDistribution[specie]):
			newGenomes[counter] = crossover(select(spciesAsLists[specie]), select(spciesAsLists[specie]))
	
	population.genomes = newGenomes
