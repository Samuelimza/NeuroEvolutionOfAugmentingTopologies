from neat import config
from neat.gene import NodeGene, ConnectionGene

class Genome():
	def __init__(self):
		self.nextNodeKey = None
		self.nodeGenes = self.createNodeGenes()
		self.connectionGenes = self.createConnectionGenes()
		self.species = 1

	def createNodeGenes(self):
		'''
		Creates a default node structure with configured Input and Output nodes.
		By convention Output nodes have negative keys starting from -1 and Input nodes
		have positive keys starting from 0.
		'''
		nodeGenes = {}
		for nodeKey in range(config.noOfOutputNodes):
			nodeGenes[-(nodeKey + 1)] = NodeGene(-(nodeKey + 1), 'OUTPUT', config.outputNodeActivation)

		for nodeKey in range(config.noOfInputNodes):
			nodeGenes[nodeKey] = NodeGene(nodeKey, 'INPUT', None)
		self.nextNodeKey = config.noOfInputNodes
		return nodeGenes

	def createConnectionGenes(self):
		'''
		Creates connections connecting the default input and output nodes with connection
		key as the innovation number. Each connection supplying a particular node has it's
		key stored in that node so the nodes supplying that particular node can be traced and
		their value can be calculatd recursively by the neural network.
		'''
		connectionGenes = {}
		connectionKey = 0
		for outputNodeKey in range(-1, (config.noOfOutputNodes + 1), -1):
			for inputNodeKey in range(config.noOfInputNodes):
				connectionGenes[connectionKey] = ConnectionGene(
					inputNodeKey,
					outputNodeKey,
					1.0,  # Use random weight here
					True,
					connectionKey
				)
				self.nodeGenes[outputNodeKey].supplyingConnectionGenes.append(conncetionKey)
				connectionKey += 1
		
		if config.GlobalInnovationCounter == 0:
			config.GlobalInnovationCounter = connectionKey
		return connectionGenes
