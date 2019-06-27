from neat import config
from neat.population import Population

def speciate(population, fitness):
	speciesAsLists = {}
	
	# Assign species to current population
	for genome in population.genomes:
		for specieRepresentative in population.speciesRepresentatives:
			if genomeDistance(genome, specieRepresentative) < config.delta:
				genome.species = speciesRepresentative.species
				if genome.specie not in speciesAsLists.keys():
					speciesAsLists[genome.specie] = []
				speciesAsLists[genome.specie].append(genome)
				break
		
		if genome.species = None:
			population.speciesRepresentatives.append(genome)
			genome.species = (population.species + 1)
			population.species += 1
			
			speciesAsLists[genome.species] = []
			speciesAsLists[genome.species].append(genome)
	
	# Assign speciesRepresentatives (from current generation) for next generation
	population.speciesRepresentatives = []
	for specieNumber in speciesAsLists.keys():
		population.speciesRepresentatives.append(random.choice(speciesAsLists[specieNumber]))

def genomeDistance(genome1, genome2):
	c1, c2 = 1, 1 # TODO: Make configurable
	innovationNumbersGenome1 = sorted(genome1.connectionGenes.keys())
	innovationNumbersGenome2 = sorted(genome2.connectionGenes.keys())
	
	# Calculate the Sum of disjoint and excess genes
	disjointAndExcessGenes = 0
	averageWeightDifference = 0
	if innovationNumbersGenome1[0] != innovationNumbersGenome2[0]:
		disjointAndExcessGenes = len(innovationNumbersGenome1) + len(innovationNumbersGenome2)
	else:
		i, j = 1, 1
		a = innovationNumbersGenome1[-i]
		b = innovationNumbersGenome2[-j]
		while True:
			if a == b:
				break
			elif a > b:
				i += 1
				a = innovationNumbersGenome1[-i]
				disjointAndExcessGenes += 1
			else:
				j += 1
				b = innovationNumbersGenome2[-j]
				disjointAndExcessGenes += 1
		
		# Calculate the average weight difference of matching genes
		if len(innovationNumbersGenome1) - i != len(innovationNumbersGenome2) - j:
			raise ValueError('Matching genes are not same in both genomes!')
		noOfMatchingGenes = (len(innovationNumbersGenome1) - i) + 1
		summation = 0
		for counter in range(noOfMatchingGenes):
			summation += abs(genome1.connectionGenes[counter].weight - genome2.connectionGenes[counter].weight)
		averageWeightDifference = summation / noOfMatchingGenes
	distance = c1 * disjointAndExcessGenes + c2 * averageWeightDifference
	return distance
