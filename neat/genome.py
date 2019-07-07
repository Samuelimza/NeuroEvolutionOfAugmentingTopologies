from copy import copy, deepcopy
import random
from . import config
from .gene import NodeGene, ConnectionGene
from .utilityClasses import Mutation


class Genome:
	def __init__(self):
		self.nextNodeKey = None
		self.nodeGenes = self.createNodeGenes()
		self.connectionGenes = self.createConnectionGenes()
		self.species = None
		self.fitness = None
		self.fullyConnected = False

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
		self.fullyConnected = True
		return connectionGenes

	def addConnection(self, inNodeKey, outNodeKey, weight, enabled, innovationNumber):
		self.connectionGenes[innovationNumber] = ConnectionGene(
			inNodeKey,
			outNodeKey,
			weight,
			enabled,
			innovationNumber
		)
		self.nodeGenes[outNodeKey].supplyingConnectionGenes.append(innovationNumber)

	@classmethod
	def crossover(cls, genome1, genome2):
		if genome1.fitness > genome2.fitness:
			genome = deepcopy(genome1)
		else:
			genome = deepcopy(genome2)
		genome.fitness = None
		genome.species = None
		# Actual crossover
		# TODO: (CLEAN) Please clean this!!!!. Also connectionKey is innovationNumber and innovationNumber is connectionKey
		connectionKey = 0
		try:
			while genome1.connectionGenes[connectionKey].innovationNumber == genome2.connectionGenes[connectionKey].innovationNumber:
				genome.connectionGenes[connectionKey].weight = random.choice(
					[genome1.connectionGenes[connectionKey].weight, genome2.connectionGenes[connectionKey].weight])
				genome.connectionGenes[connectionKey].enabled = random.choice(
					[genome1.connectionGenes[connectionKey].enabled, genome2.connectionGenes[connectionKey].enabled])
				connectionKey += 1
		except KeyError:
			pass
		return genome

	def mutate(self, connectionMutations, nodeMutations):
		# TODO: (FEATURE) Add different mutation controls such as: only one structural mutation or all
		if random.random() < config.mutateAddConnection and not self.fullyConnected:
			self.mutateAddConnection(connectionMutations)
		if random.random() < config.mutateAddNode:
			self.mutateAddNode(nodeMutations)
		if random.random() < config.mutateChangeWeight:
			self.mutateChangeWeight()
		if random.random() < config.mutateEnableGene:
			# self.mutateEnableConnection()
			pass

	def mutateAddConnection(self, connectionMutations):
		inKeys = [k for k in self.nodeGenes.keys()]
		outKeys = inKeys
		random.shuffle(inKeys)
		random.shuffle(outKeys)
		for inNodeKey in inKeys:
			for outNodeKey in outKeys:
				# Conditions here to make sure that forward propagating connections are evolved only
				valid = inNodeKey != outNodeKey and self.nodeGenes[inNodeKey].nodeType != 'OUTPUT' and self.nodeGenes[outNodeKey].nodeType != 'INPUT'
				cyclic = self.isCyclic(inNodeKey, outNodeKey)
				alreadyExists = False
				for connection in self.connectionGenes:
					if self.connectionGenes[connection].inNodeKey == inNodeKey and self.connectionGenes[connection].outNodeKey == outNodeKey:
						alreadyExists = True
						break

				if valid and not cyclic and not alreadyExists:
					innovationNumber = None
					for mutation in connectionMutations:
						if inNodeKey == mutation.inNodeKey and outNodeKey == mutation.outNodeKey:
							innovationNumber = mutation.innovationNumber
					if innovationNumber is None:
						innovationNumber = config.GlobalInnovationCounter
						config.GlobalInnovationCounter += 1
						connectionMutations.append(Mutation(inNodeKey = inNodeKey, outNodeKey = outNodeKey, innovationNumber = innovationNumber))
					self.addConnection(
						inNodeKey,
						outNodeKey,
						(random.random() * 2) - 1,
						True,
						innovationNumber
					)
					return
		self.fullyConnected = True

	def mutateAddNode(self, nodeMutations):
		# TODO: (IMPORTANT) Add innovation tracking capability for the current generation so as to limit globalInnovationCounter
		connectionKey = None
		keys = [k for k in self.connectionGenes]
		random.shuffle(keys)
		for key in keys:
			if self.connectionGenes[key].enabled:
				connectionKey = key
		if connectionKey is None:
			self.printDetails()
			raise ValueError('Connection key is none node cannot be added')
		newNode = NodeGene(self.nextNodeKey, 'HIDDEN', config.hiddenNodeActivation)
		self.nextNodeKey += 1
		connection0 = ConnectionGene(self.connectionGenes[connectionKey].inNodeKey, newNode.nodeNumber,
									 self.connectionGenes[connectionKey].weight, True, config.GlobalInnovationCounter)
		config.GlobalInnovationCounter += 1
		connection1 = ConnectionGene(newNode.nodeNumber, self.connectionGenes[connectionKey].outNodeKey, 1.0, True,
									 config.GlobalInnovationCounter)
		config.GlobalInnovationCounter += 1

		# Add new connections to the respective node for tracking in supplyingConnectionGenes
		newNode.supplyingConnectionGenes.append(connection0.innovationNumber)
		self.nodeGenes[self.connectionGenes[connectionKey].outNodeKey].supplyingConnectionGenes.append(
			connection1.innovationNumber)

		self.connectionGenes[connectionKey].enabled = False

		# Finally adding genes to the genome
		self.nodeGenes[newNode.nodeNumber] = newNode
		self.connectionGenes[connection0.innovationNumber] = connection0
		self.connectionGenes[connection1.innovationNumber] = connection1

	def mutateChangeWeight(self):
		for connection in self.connectionGenes:
			if self.connectionGenes[connection].enabled:
				nudge = random.random() - 0.5
				self.connectionGenes[connection].weight += nudge

	def mutateEnableConnection(self):
		disabledConnectionKey = None
		condition = True
		# TODO: (CLEAN) Randomize the connection chosen not just the first found
		while condition:
			disabledConnectionKey = random.choice([k for k in self.connectionGenes])
			condition = self.connectionGenes[disabledConnectionKey].enabled

		self.connectionGenes[disabledConnectionKey].enabled = True

	def isCyclic(self, inNodeKey, outNodeKey):
		this = deepcopy(self)
		this.connectionGenes[config.GlobalInnovationCounter] = ConnectionGene(
			inNodeKey,
			outNodeKey,
			1,
			True,
			config.GlobalInnovationCounter
		)
		this.nodeGenes[outNodeKey].supplyingConnectionGenes.append(config.GlobalInnovationCounter)

		def dfs(node, stack):
			if this.nodeGenes[node].nodeType == 'INPUT':
				return False
			if node in stack:
				return True
			stack.append(node)
			for connection in this.nodeGenes[node].supplyingConnectionGenes:
				if dfs(this.connectionGenes[connection].inNodeKey, stack):
					return True
			stack.pop()
			return False
		realStack = []
		# Should this be inNodeKey or outNodeKey, does it even matter??
		return dfs(inNodeKey, realStack)

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

		# Weird way to print hidden nodes TODO: (CLEAN) please fix
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
			else:
				print("\t", connectionKey, "DISABLED_CONNECTION:", self.connectionGenes[connectionKey].printDetails())
		print("Genome printed")
