import random
from neat import config
from neat.genome import Genome

class Population():
	def __init__(self):
		self.species = []
		species.append([])
		for i in range(config.populationSize):
			self.species[0].append(Genome())
		self.speciesTracker = [random.choice(self.species[0])]
