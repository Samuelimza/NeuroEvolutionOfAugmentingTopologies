import random
from neat import config
from neat.genome import Genome

class Population():
	def __init__(self, default = True):
		self.genomes = []
		self.specieRepresentatives = []
		if default:
			initialize()
		
	def initialize():
		for i in range(config.populationSize):
			self.genomes.append(Genome())
		self.specieRepresentatives.append(random.choice(self.genomes))
