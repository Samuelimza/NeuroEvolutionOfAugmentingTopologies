class Mutation:
	"""
	Class Mutation: Used to describe node and connection mutations that are tracked duting reproduction phase.
	"""
	def __init__(self, inNodeKey = None, outNodeKey = None, innovationNumber_s = None):
		self.inNodeKey = inNodeKey
		self.outNodeKey = outNodeKey
		self.innovationNumber_s = innovationNumber_s


class ConnectionGene:
	"""
	Class ConnectionGene: Data Struct for a single connection gene.
	"""
	def __init__(self, inNodeKey, outNodeKey, weight, enabled, innovationNumber):
		self.inNodeKey = inNodeKey
		self.outNodeKey = outNodeKey
		self.weight = weight
		self.enabled = enabled
		self.innovationNumber = innovationNumber

	def printDetails(self):
		return "({0})>--[{1:.3f}]-->({2})".format(self.inNodeKey, self.weight, self.outNodeKey)


class NodeGene:
	"""
	Class NodeGene: Data Struct for a single node gene.
	"""
	def __init__(self, nodeNumber, nodeType, activationFunction):
		self.nodeNumber = nodeNumber
		self.nodeType = nodeType
		self.activationFunction = activationFunction
		self.supplyingConnectionGenes = []
		# TODO: Randomize bias initialisation
		self.bias = 0.0

	def printDetails(self):
		return "({}), Bias = {:.3f}".format(self.nodeNumber, self.bias)


class Reporter:
	"""
	Class Reporter: Reporter for various statistics throughout the evolution of the population
	"""
	def __init__(self, totalGenerations):
		self.generation = 0
		self.maxFitness = []
		self.speciesWiseFitness = []  # dictionary[generation][specie] == maxFitnessOfThatSpecieThatGeneration
		self.totalGenerations = totalGenerations
		self.stolenBabies = 0
		self.timing = None
		self.speciesSorted = None
		self.obliteratedSpecies = []
		self.extinctSpecies = []

	def showGeneration(self, speciesAsLists):
		print(" ")
		print("####################################################################################################################")
		for specie in self.speciesSorted:
			print("Specie = ", specie)
			for genome in speciesAsLists[specie]:
				print("\tGenome: {:3d}, nodes: {:3d}, connections: {:3d}".format(genome.originalCounter, len(genome.nodeGenes), len(genome.connectionGenes)), end=" ")
				if genome.output is not None:
					print(" ,fitness: {:.2f}, output: [ ".format(genome.originalFitness), end="")
					for x in range(len(genome.output)):
						print("{:.2f} ".format(genome.output[x][0]), end="")
					print("]")
				else:
					print(" ,fitness: {:.2f}".format(genome.originalFitness))
		if len(self.obliteratedSpecies) > 0:
			print("Obliterated species:", end=" ")
			for specie in self.obliteratedSpecies:
				print(specie, end=" ")
			print(" ")
		if len(self.extinctSpecies) > 0:
			print("Extinct species: ", end=" ")
			for specie in self.extinctSpecies:
				print(specie, end=" ")
			print(" ")
		print('Generation: ', self.generation, 'Max fitness: ', speciesAsLists[self.speciesSorted[0]][0].originalFitness, ', Of genome: ', speciesAsLists[self.speciesSorted[0]][0].originalCounter)
		print("Stolen Babies: ", self.stolenBabies)
		print("Total Generation Timing {0:.2f}: {1:.1f}% fitnessEvaluation, {2:.1f}% speciation, {3:.1f}% reproduction, {4:.1f}% wasted".format(self.timing[3], self.timing[0] / self.timing[3], self.timing[1] / self.timing[3], self.timing[2] / self.timing[3], self.timing[3] - (self.timing[0] + self.timing[1] + self.timing[2])))
		print("####################################################################################################################")
		print(" ")
		self.extinctSpecies = []
		self.obliteratedSpecies = []

	def showStatistics(self, plt):
		gen = [i for i in range(self.generation + 1)]
		plt.plot(gen, self.maxFitness)
		plt.show()
