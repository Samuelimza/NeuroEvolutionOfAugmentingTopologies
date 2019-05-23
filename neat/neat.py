class neatclass():
	def __init__(self, function):
		self.fitnessFunction = function

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
		self.fitnessFunction(giveNNs(population))
		self.speciate(self.population)
		parents = self.select(self.population)
		self.population = self.crossover(parents)
		self.mutate(self.population)

	def giveNNs(self, population):
		neuralNetworks = []
		for genome in population:
			neuralNetworks.append(NeuralNetwork(genome))
		return neuralNetworks
