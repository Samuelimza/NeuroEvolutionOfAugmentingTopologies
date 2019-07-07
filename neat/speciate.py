import random
from . import config
from .population import Population


def speciate(population):
    speciesAsLists = {}

    # Assign species to current population
    for genome in population.genomes:
        for specieRepresentative in population.speciesRepresentatives:
            if genomeDistance(genome, specieRepresentative) < config.delta:
                genome.species = specieRepresentative.species
                if genome.species not in speciesAsLists.keys():
                    speciesAsLists[genome.species] = []
                speciesAsLists[genome.species].append(genome)
                break

        if genome.species == None:
            population.speciesRepresentatives.append(genome)
            genome.species = (population.species + 1)
            population.species += 1

            speciesAsLists[genome.species] = []
            speciesAsLists[genome.species].append(genome)

    # Assign speciesRepresentatives (from current generation) for next generation
    population.speciesRepresentatives = []
    for specieNumber in speciesAsLists.keys():
        population.speciesRepresentatives.append(random.choice(speciesAsLists[specieNumber]))

    return speciesAsLists


def genomeDistance(genome1, genome2):
    c1, c2 = 1, 0.5  # TODO: Make configurable
    innovationNumbersGenome1 = sorted(genome1.connectionGenes.keys())
    innovationNumbersGenome2 = sorted(genome2.connectionGenes.keys())

    # Calculate the Sum of disjoint and excess genes
    disjointAndExcessGenes = 0
    averageWeightDifference = 0
    if innovationNumbersGenome1[0] != innovationNumbersGenome2[0]:
        disjointAndExcessGenes = len(innovationNumbersGenome1) + len(innovationNumbersGenome2)
    else:
        i, j = 0, 0
        matchingInnovNumbers = []
        while i < len(innovationNumbersGenome1) and j < len(innovationNumbersGenome2):
            a = innovationNumbersGenome1[i]
            b = innovationNumbersGenome2[j]
            if a == b:
                matchingInnovNumbers.append(a)
                i += 1
                j += 1
            elif a > b:
                i += 1
                disjointAndExcessGenes += 1
            else:
                j += 1
                disjointAndExcessGenes += 1

        summation = 0
        for innovNumber in matchingInnovNumbers:
            summation += abs(genome1.connectionGenes[innovNumber].weight - genome2.connectionGenes[innovNumber].weight)
        averageWeightDifference = summation / (len(matchingInnovNumbers) - 1)
    distance = c1 * disjointAndExcessGenes + c2 * averageWeightDifference
    return distance
