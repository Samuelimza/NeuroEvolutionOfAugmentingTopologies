from . import config
from .neuralNetwork import NeuralNetwork
from .population import Population
from .speciate import speciate
from .reproduce import reproduce
from .genome import Genome

class NEAT():
	def __init__(self, function):
		self.fitnessFunction = function
		self.population = Population()

	def train(self):
		'''
		Core Evolutionary algoroithm of neat
		'''
		for i in range(config.totalGenerations):
			print("Generation: {}".format(i))
			print("\tGenomes: {}".format(len(self.population.genomes)))
			fitness = self.fitnessFunction(self.convertToNeuralNetwork(self.population))
			speciesAsLists = speciate(self.population)
			reproduce(self.population, speciesAsLists, fitness)
		
		return self.population.genomes

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
			for genome in sample.genomes:
				neuralNetworks.append(NeuralNetwork(genome))
			return neuralNetworks
		else:
			raise TypeError(
				'Argument passed must be of one of the following types: \
				Genome, list of Genomes or Population'
			)

