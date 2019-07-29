from . import config
from .genome import Genome


def speciate(population):
    speciesAsLists = {}
    newSpeciesRepresentatives = []
    newSpecies = []

    # Assign species to current population
    for genome in population.genomes:
        genome.species = None
        for specieRepresentative in population.speciesRepresentatives:
            if Genome.genomeDistance(genome, specieRepresentative) < config.delta:
                genome.species = specieRepresentative.species
                if genome.species not in speciesAsLists.keys():
                    speciesAsLists[genome.species] = []
                speciesAsLists[genome.species].append(genome)
                break

        if genome.species is None:
            genome.species = (population.species + 1)
            population.species += 1

            population.speciesRepresentatives.append(genome)
            newSpeciesRepresentatives.append(genome)
            newSpecies.append(genome.species)

            speciesAsLists[genome.species] = []
            speciesAsLists[genome.species].append(genome)
        if genome.species not in speciesAsLists.keys():
            raise ValueError("SpeciationError")

    # Assign speciesRepresentatives (from current generation) for next generation
    population.speciesRepresentatives = [*newSpeciesRepresentatives]
    for specieNumber in speciesAsLists.keys():
        if specieNumber in newSpecies:
            continue
        population.speciesRepresentatives.append(config.random.choice(speciesAsLists[specieNumber]))

    return speciesAsLists
