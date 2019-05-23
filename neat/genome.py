class Genome():
	def __init__(self):
		self.lastNodeKey = None
		self.nodeGenes = createNodeGenes()
		self.connectionGenes = connectionGenes
		self.species = species

	def createNodeGenes(self):
		'''
		Creates a default node structure with configured Input and Output nodes.
		By convention Output nodes have negative keys starting from -1 and Input nodes
		have positive keys starting from 0.
		'''
		nodeGenes = {}
		for nodeKey in range(config['noOfOutputNodes']):
			self.nodeGenes[-(nodeKey + 1)] = NodeGene(-(nodeKey + 1), 'OUTPUT',
			config['outputNodeActivation'])

		for nodeKey in range(config['noOfInputNodes']):
			self.nodeGenes[nodeKey] = NodeGene(nodeKey, 'INPUT', None)
		self.lastNodeKey = config['noOfInputNodes'] - 1
		return nodeGenes

	def createConnectionGenes(self):
		connectionGenes = {}
