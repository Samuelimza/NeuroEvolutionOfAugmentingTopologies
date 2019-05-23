class NeuralNetwork():
	def self.__init__(self, genome):
		self.genome = genome

	def activate(self, inputs):
		outputs = []
		for outputNodeKey in config['noOfOutputNodes']:
			outputs.append(self.value(-(outputNodeKey + 1)))
		return outputs
	
	def value(self, nodeKey):
		if self.genome.nodeGenes[nodeKey].nodeType is 'INPUT':
			return inputs[node.nodeNumber]
		thisValue = 0
		for subNode in node.dependencies:
			thisValue += self.value(subNode)
		return activationFunctions[self.genome.nodeGenes[nodeKey].activationFunction](thisValue)
