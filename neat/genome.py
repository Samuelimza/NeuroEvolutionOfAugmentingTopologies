class Genome():
	def __init__(self, config):
		self.nodeGenes = createNodeGenes(config)
		self.connectionGenes = connectionGenes
		self.species = species

	def createNodeGenes(self, config):
		nodeGenes = []
		for nodeKey in config['noOfInputNodes']:
			self.nodeGenes[nodeKey] = NodeGene(nodeKey, 'INPUT')

		for nodeKey in config['noOfOutputNodes']:
			modifiedNodeKey = nodeKey + len(self.nodeGenes)
			self.nodeGenes[modifiedNodeKey] = NodeGene(modifiedNodeKey, 'OUTPUT')
		return nodeGenes()

	def createConnectionGenes(self, config):
		connectionGenes = []
