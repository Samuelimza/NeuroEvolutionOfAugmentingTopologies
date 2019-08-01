class Mutation:
	def __init__(self, inNodeKey = None, outNodeKey = None, innovationNumber_s = None):
		self.inNodeKey = inNodeKey
		self.outNodeKey = outNodeKey
		self.innovationNumber_s = innovationNumber_s


class ConnectionGene:
	def __init__(self, inNodeKey, outNodeKey, weight, enabled, innovationNumber):
		self.inNodeKey = inNodeKey
		self.outNodeKey = outNodeKey
		self.weight = weight
		self.enabled = enabled
		self.innovationNumber = innovationNumber

	def printDetails(self):
		return "({0})>--[{1:.3f}]-->({2})".format(self.inNodeKey, self.weight, self.outNodeKey)


class NodeGene:
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
	def __init__(self, totalGenerations):
		self.generation = 0
		self.maxFitness = []
		self.speciesWiseFitness = []  # dictionary[generation][specie] == maxFitnessOfThatSpecieThatGeneration
		self.totalGenerations = totalGenerations

	def showStatistics(self, plt):
		gen = [i for i in range(self.generation)]
		plt.plot(gen, self.maxFitness)
		plt.show()
