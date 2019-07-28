from . import config
from .genome import Genome


def speciate(population):
    speciesAsLists = {}

    # Assign species to current population
    for genome in population.genomes:
        for specieRepresentative in population.speciesRepresentatives:
            if Genome.genomeDistance(genome, specieRepresentative) < config.delta:
                genome.species = specieRepresentative.species
                if genome.species not in speciesAsLists.keys():
                    speciesAsLists[genome.species] = []
                speciesAsLists[genome.species].append(genome)
                break

        if genome.species is None:
            population.speciesRepresentatives.append(genome)
            genome.species = (population.species + 1)
            population.species += 1

            speciesAsLists[genome.species] = []
            speciesAsLists[genome.species].append(genome)

    # Assign speciesRepresentatives (from current generation) for next generation
    population.speciesRepresentatives = []
    for specieNumber in speciesAsLists.keys():
        population.speciesRepresentatives.append(config.random.choice(speciesAsLists[specieNumber]))

    return speciesAsLists
