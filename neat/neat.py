class neatclass():
	def __init__(self, function):
		self.fitnessFunction = function

	def speciate():
		pass

	def select():
		pass

	def crossover():
		pass

	def mutate():
		pass

	def train():
		self.fitnessFunction(giveNNs(population))
		self.speciate(self.population)
		parents = self.select(self.population)
		self.population = self.crossover(parents)
		self.mutate(self.poplation)

	def giveNNs():
		pass
