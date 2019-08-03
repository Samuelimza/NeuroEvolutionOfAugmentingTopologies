from . import config
from .neuralNetwork import NeuralNetwork
from .population import Population
from .speciate import speciate
from .reproduce import reproduce
from .genome import Genome
from .utilityClasses import Reporter
import matplotlib.pyplot as plt
import time


class NEAT:
	def __init__(self, function):
		self.fitnessFunction = function
		self.population = Population()

	def train(self):
		reporter = Reporter(config.totalGenerations)

		# Core Evolutionary algorithm of neat
		for i in range(config.totalGenerations):
			reporter.generation = i
			TIC = time.time()
			tic = time.time()
			fitness = self.fitnessFunction(self.convertToNeuralNetwork(self.population))
			fitnessTiming = time.time() - tic
			maxFitness = max(fitness)
			index = fitness.index(maxFitness)
			reporter.maxFitness.append(maxFitness)
			print('Generation: ', i, 'Max fitness: ', maxFitness, ', Of genome: ', index)
			self.population.genomes[index].printDetails()
			tic = time.time()
			speciesAsLists = speciate(self.population)
			speciationTiming = time.time() - tic
			tic = time.time()
			reproduce(self.population, speciesAsLists, fitness, reporter)
			reproductionTiming = time.time() - tic
			totalTime = time.time() - TIC
			print("Total Generation Timing {0:.2f}: {1:.1f}% fitnessEvaluation, {2:.1f}% speciation, {3:.1f}% reproduction, {4:.1f}% wasted".format(totalTime, fitnessTiming / totalTime, speciationTiming / totalTime, reproductionTiming / totalTime, totalTime - (fitnessTiming + speciationTiming + reproductionTiming)))

		reporter.showStatistics(plt)
		return self.population.genomes

	def convertToNeuralNetwork(self, sample):
		# API method used to convert genotypes(genomes) to phenotypes(Neural Networks)
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
