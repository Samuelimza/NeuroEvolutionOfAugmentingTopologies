from . import config

class NeuralNetwork():
	def __init__(self, genome):
		self.genome = genome

	def activate(self, inputs):
		outputs = []
		
		#Recursive function to evaluate node values in the graph network
		def value(nodeKey):
			if self.genome.nodeGenes[nodeKey].nodeType is 'INPUT':
				return inputs[self.genome.nodeGenes[nodeKey].nodeNumber]
			thisValue = 0
			for key in self.genome.nodeGenes[nodeKey].supplyingConnectionGenes:
				if self.genome.connectionGenes[key].enabled:
					thisValue += self.genome.connectionGenes[key].weight * value(self.genome.connectionGenes[key].inNodeKey)
			
			return config.activationFunctions[self.genome.nodeGenes[nodeKey].activationFunction](thisValue)
		
		for outputNodeKey in range(config.noOfOutputNodes):
			outputs.append(value(-(outputNodeKey + 1)))
		return outputs
