from . import config


class NeuralNetwork():
	def __init__(self, genome):
		self.genome = genome

	def activate(self, inputs):
		"""
		inputs: Numpy array of shape (m, noOfInputNodes)
		output: Numpy array of shape (m, noOfOutputNodes)
		"""
		output = []
		for i in range(len(inputs)):
			outputs = []
			for outputNodeKey in range(config.noOfOutputNodes):
				outputs.append(self.value(-(outputNodeKey + 1), inputs[i]))
			output.append(outputs)
		return output

	#
	def value(self, nodeKey, trainingExample):
		"""
		Recursive function to evaluate node values in the graph network

		Parameters:
			nodeKey: The node key of the node to be evaluated (To evaluate output of network, node key is an output node key)
			trainingExample: A single set of inputs for the input nodes
		Returns:
			value of the output node evaluated at the input
		"""
		if self.genome.nodeGenes[nodeKey].nodeType is 'INPUT':
			return trainingExample[self.genome.nodeGenes[nodeKey].nodeNumber]
		thisValue = 0
		for key in self.genome.nodeGenes[nodeKey].supplyingConnectionGenes:
			if self.genome.connectionGenes[key].enabled:
				thisValue += self.genome.connectionGenes[key].weight * self.value(
					self.genome.connectionGenes[key].inNodeKey,
					trainingExample
				)
		thisValue += self.genome.nodeGenes[nodeKey].bias
		return config.activationFunctions[self.genome.nodeGenes[nodeKey].activationFunction](thisValue)
