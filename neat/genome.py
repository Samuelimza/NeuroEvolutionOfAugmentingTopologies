from copy import copy, deepcopy
import random
from . import config
from .gene import NodeGene, ConnectionGene

class Genome():
	def __init__(self):
		self.nextNodeKey = None
		self.nodeGenes = self.createNodeGenes()
		self.connectionGenes = self.createConnectionGenes()
		self.species = None
		self.fitness = None

	def createNodeGenes(self):
		'''
		Creates a default node structure with configured Input and Output nodes.
		By convention Output nodes have negative keys starting from -1 and Input nodes
		have positive keys starting from 0.
		'''
		nodeGenes = {}
		for nodeKey in range(config.noOfOutputNodes):
			nodeGenes[-(nodeKey + 1)] = NodeGene(
				-(nodeKey + 1),
				'OUTPUT',
				config.outputNodeActivation
			)

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
		for outputNodeKey in range(-1, -(config.noOfOutputNodes + 1), -1):
			for inputNodeKey in range(config.noOfInputNodes):
				connectionGenes[connectionKey] = ConnectionGene(
					inputNodeKey,
					outputNodeKey,
					(random.random() * 2) - 1,  # Use random weight here
					True,
					connectionKey
				)
				self.nodeGenes[outputNodeKey].supplyingConnectionGenes.append(connectionKey)
				connectionKey += 1
		
		if config.GlobalInnovationCounter == 0:
			config.GlobalInnovationCounter = connectionKey
		return connectionGenes
	
	@classmethod
	def crossover(cls, genome1, genome2):
		if genome1.fitness > genome2.fitness:
			genome = deepcopy(genome1)
		else:
			genome = deepcopy(genome2)
		# Actual crossover
		connectionKey = 0
		while genome1.connectionGenes[connectionKey].innovationNumber == genome2.connectionGenes[connectionKey].innovationNumber:
			genome.connectionGenes[connectionKey].weight = random.choice(genome1.connectionGenes[connectionKey].weight, genome2.connectionGenes[connectionKey].weight)
			genome.connectionGenes[connectionKey].enabled = random.choice(genome1.connectionGenes[connectionKey].enabled, genome2.connectionGenes[connectionKey].enabled)
			connectionKey += 1
		return genome

	def mutate(self):
		if random.random() < config.mutateAddConnection:
			self.addConnection()
		if random.random() < config.mutateAddNode:
			self.addNode()
		if random.random() < config.mutateChangeWeight:
			self.changeWeight()
		if random.random() < config.mutateEnableGene:
			self.enableConnection()
	
	def addConnection():
		while not condition:
			inNodeKey = random.choice(self.nodeGenes.keys())
			outNodeKey = random.choice(self.nodeGenes.keys())
			condition1 = inNodeKey != outNodeKey
			'''
			Conditions here to make sure that forward propagating connections are evolved only
			TODO: Add additional condition that checks if the connection doesn't already exist
			TODO: Implement way to check this mutation against possibly same mutations later in this generation
			'''
			condition2 = (self.nodeGenes[inNodeKey].nodeType == 'INPUT') or (self.nodeGenes[inNodeKey].nodeType == 'HIDDEN')
			condition3 = (self.nodeGenes[outNodeKey].nodeType == 'HIDDEN') or (self.nodeGenes[outNodeKey].nodeType == 'OUTPUT')
			condition = condition1 and condition2 and condition3
		
		self.connectionGenes[config.globalInnovationNumber] = ConnectionGene(
			inNodeKey,
			outNodeKey,
			(2 * random()) - 1,
			True,
			config.globalInnovationNumber
		)
		self.nodeGenes[outNodeKey].supplyingConnectionGenes.append(config.globalInnovationNumber)
		config.globalInnovationNumber += 1
	
	# Do something for this ugly visualisation function please
	def printDetails(self):
		print("Printing Genome")
		print("Number of Node Genes = ", len(self.nodeGenes))
		for outputNodeKey in range(-1, -(config.noOfOutputNodes + 1), -1):
			print("OUTPUT NODE:", self.nodeGenes[outputNodeKey].printDetails())
		for inputNodeKey in range(config.noOfInputNodes):
			print("INPUT NODE:", self.nodeGenes[inputNodeKey].printDetails())
		print("Number of Connection Genes = ", len(self.connectionGenes))
		for connectionKey in range(len(self.connectionGenes)):
			print("CONNECTION:", self.connectionGenes[connectionKey].printDetails())
		print("Genome printed")
