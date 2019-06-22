from neat import config
from neat.neuralNetwork import NeuralNetwork
from neat.population import Population
from neat.genome import Genome

class NEAT():
	def __init__(self, function):
		self.fitnessFunction = function
		self.population = Population()

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
		population = speciate(self.population, fitness)
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
			for species in population.species:
				for genome in species:
					neuralNetworks.append(NeuralNetwork(genome))
			return neuralNetworks
		else:
			raise TypeError(
				'Argument passed must be of one of the following types: \
				Genome, list of Genomes or Population'
			)
