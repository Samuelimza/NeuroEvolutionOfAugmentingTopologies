from neat import config
from neat.genome import Genome

class NEAT():
	def __init__(self, function):
		self.fitnessFunction = function
		self.population = []
		
		for i in range(config.populationSize):
			self.population.append(Genome())

	def speciate(self):
		pass

	def select(self):
		pass

	def crossover(self):
		pass

	def mutate(self):
		pass

	def train(self):
		'''
		Core Evolutionary algoroithm of neat
		'''
		fitness = self.fitnessFunction(giveNNs(self.population))
		self.speciate(self.population, fitness)
		parents = self.select(self.population)
		self.population = self.crossover(parents)
		self.mutate(self.population)

	def giveNNs(self, population):
		'''
		API method used to convert genotypes(genomes) to phenotypes(Neural Networks)
		'''
		neuralNetworks = []
		for genome in population:
			neuralNetworks.append(NeuralNetwork(genome))
		return neuralNetworks
