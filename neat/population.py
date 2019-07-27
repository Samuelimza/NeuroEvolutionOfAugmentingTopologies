from . import config
from .genome import Genome


class Population():
    def __init__(self, random, default=True):
        self.genomes = []
        self.speciesRepresentatives = []
        self.species = 0
        self.random = random
        if default:
            self.initialize()

    def initialize(self):
        for i in range(config.populationSize):
            self.genomes.append(Genome(self.random))
