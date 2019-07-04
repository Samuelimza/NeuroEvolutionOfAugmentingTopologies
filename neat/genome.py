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
		genome.fitness = None
		genome.species = None
		# Actual crossover
		# Please clean this!!!!. Also connectionKey is innovationNumber and innovationNumber is connectionKey
		connectionKey = 0
		try:
			while genome1.connectionGenes[connectionKey].innovationNumber == genome2.connectionGenes[connectionKey].innovationNumber:
				genome.connectionGenes[connectionKey].weight = random.choice([genome1.connectionGenes[connectionKey].weight, genome2.connectionGenes[connectionKey].weight])
				genome.connectionGenes[connectionKey].enabled = random.choice([genome1.connectionGenes[connectionKey].enabled, genome2.connectionGenes[connectionKey].enabled])
				connectionKey += 1		
		except KeyError:
			pass
		return genome

	def mutate(self):
		# TODO: Add different mutation controls such as: only one structural mutation or all
		if random.random() < config.mutateAddConnection:
			self.addConnection()
		if random.random() < config.mutateAddNode:
			self.addNode()
		if random.random() < config.mutateChangeWeight:
			self.changeWeight()
		if random.random() < config.mutateEnableGene:
			# self.enableConnection()
			pass
	
	def addConnection(self):
		condition = False
		while not condition:
			inNodeKey = random.choice([k for k in self.nodeGenes.keys()])
			outNodeKey = random.choice([k for k in self.nodeGenes.keys()])
			condition1 = inNodeKey != outNodeKey
			'''
			Conditions here to make sure that forward propagating connections are evolved only
			TODO: Add additional condition that checks if the connection doesn't already exist
			TODO: Implement way to check this mutation against possibly same mutations later in this generation
			'''
			condition2 = (self.nodeGenes[inNodeKey].nodeType == 'INPUT') or (self.nodeGenes[inNodeKey].nodeType == 'HIDDEN')
			condition3 = (self.nodeGenes[outNodeKey].nodeType == 'HIDDEN') or (self.nodeGenes[outNodeKey].nodeType == 'OUTPUT')
			condition = condition1 and condition2 and condition3
		
		self.connectionGenes[config.GlobalInnovationCounter] = ConnectionGene(
			inNodeKey,
			outNodeKey,
			(2 * random.random()) - 1,
			True,
			config.GlobalInnovationCounter
		)
		self.nodeGenes[outNodeKey].supplyingConnectionGenes.append(config.GlobalInnovationCounter)
		config.GlobalInnovationCounter += 1
	
	def addNode(self):
		# TODO: Check if choden connection is not disabled
		connectionKey = random.choice([k for k in self.connectionGenes])
		newNode = NodeGene(self.nextNodeKey, 'HIDDEN', config.hiddenNodeActivation)
		self.nextNodeKey += 1
		connection0 = ConnectionGene(self.connectionGenes[connectionKey].inNodeKey, newNode.nodeNumber, self.connectionGenes[connectionKey].weight, True, config.GlobalInnovationCounter)
		config.GlobalInnovationCounter += 1
		connection1 = ConnectionGene(newNode.nodeNumber, self.connectionGenes[connectionKey].outNodeKey, 1.0, True, config.GlobalInnovationCounter)
		config.GlobalInnovationCounter += 1
		
		# Add new connections to the respective node for tracking in supplyingConnectionGenes
		newNode.supplyingConnectionGenes.append(connection0.innovationNumber)
		self.nodeGenes[self.connectionGenes[connectionKey].outNodeKey].supplyingConnectionGenes.append(connection1.innovationNumber)
		
		# NOTE: Not necessay, just ignore disabled genes in the neural network (Remove 'connection' from the supplyingGenes of connection.outNodeKey)
		self.connectionGenes[connectionKey].enabled = False
		
		# Finally adding genes to the genome
		self.nodeGenes[newNode.nodeNumber] = newNode
		self.connectionGenes[connection0.innovationNumber] = connection0
		self.connectionGenes[connection1.innovationNumber] = connection1
	
	def changeWeight(self):
		connectionKey = random.choice([k for k in self.connectionGenes])
		nudge = random.random() - 0.5
		self.connectionGenes[connectionKey].weight += nudge
	
	def enableConnection(self):
		disabledConnectionKey = None
		condition = True
		# TODO: Randomize the connection chosen not just the first found
		while condition:
			disabledConnectionKey = random.choice([k for k in self.connectionGenes])
			condition = self.connectionGenes[disabledConnectionKey].enabled
		
		self.connectionGenes[disabledConnectionKey].enabled = True
	
	# Do something for this ugly visualisation function please
	def printDetails(self):
		print("Printing Genome")
		print("Number of Node Genes = ", len(self.nodeGenes))
		for outputNodeKey in range(-1, -(config.noOfOutputNodes + 1), -1):
			print("\tOUTPUT NODE:", self.nodeGenes[outputNodeKey].printDetails())
		counter = 0
		for inputNodeKey in range(config.noOfInputNodes):
			print("\tINPUT NODE:", self.nodeGenes[inputNodeKey].printDetails())
			counter += 1
		
		# Weird way to print hidden nodes TODO: please fix
		try:
			while True:
				print("\tHIDDEN NODE:", self.nodeGenes[counter].printDetails())
				counter += 1
		except KeyError:
			pass
		
		print("Number of Connection Genes = ", len(self.connectionGenes))
		for connectionKey in self.connectionGenes:
			if self.connectionGenes[connectionKey].enabled:
				print("\t", connectionKey, "CONNECTION:", self.connectionGenes[connectionKey].printDetails())
		print("Genome printed")
