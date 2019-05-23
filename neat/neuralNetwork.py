class NeuralNetwork():
	def self.init(genome):
		self.genome = genome

	def activate(inputs):
		outputNodes = []
		inputNodes = []
		for nodeGene in self.genome.nodeGenes:
			if nodeGene.nodeType = 'OUTPUT':
				outputNodes.append(nodeGene)
			elif nodeGene.nodeType = 'INPUT':
				inputNodes.append(nodeGene)
		outputs = []
		for outputNode in outputNodes:
			outputs.append(value(outputNode))
		return outputs
	
	def value(node):
		if node.nodeType is 'INPUT':
			return inputs[node.nodeNumber]
		return value(node.dependencies)
