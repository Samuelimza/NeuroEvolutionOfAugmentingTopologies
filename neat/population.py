import random
from . import config
from .genome import Genome


class Population():
    def __init__(self, default=True):
        self.genomes = []
        self.speciesRepresentatives = []
        self.species = 0
        if default:
            self.initialize()

    def initialize(self):
        for i in range(config.populationSize):
            self.genomes.append(Genome())
