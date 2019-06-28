from . import config
from .neuralNetwork import NeuralNetwork
from .population import Population
from .speciate import speciate
from .genome import Genome

class NEAT():
	def __init__(self, function):
		self.fitnessFunction = function
		self.population = Population()

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
		fitness = self.fitnessFunction(self.convertToNeuralNetwork(self.population))
		speciesAsLists = speciate(self.population)
		reproduce(self.population, speciesAsLists, fitness)
		parents = self.select(self.population)
		self.population = self.crossover(parents)
		self.mutate(self.population)

	def convertToNeuralNetwork(self, sample):
		'''
		API method used to convert genotypes(genomes) to phenotypes(Neural Networks)
		'''
		if isinstance(sample, Genome):
			return NeuralNetwork(sample)
		elif isinstance(sample, list):
			neuralNetworks = []
			for genome in sample:
				neuralNetworks.append(NeuralNetwork(genome))
			return neuralNetworks
		elif isinstance(sample, Population):
			neuralNetworks = []
			for genome in population.genomes:
				neuralNetworks.append(NeuralNetwork(genome))
			return neuralNetworks
		else:
			raise TypeError(
				'Argument passed must be of one of the following types: \
				Genome, list of Genomes or Population'
			)
