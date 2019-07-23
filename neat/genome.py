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
		self.fullyConnected = True

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

	def addConnection(self, inNodeKey, outNodeKey, weight, enabled, innovationNumber):
		self.connectionGenes[innovationNumber] = ConnectionGene(
			inNodeKey,
			outNodeKey,
			weight,
			enabled,
			innovationNumber
		)
		self.nodeGenes[outNodeKey].supplyingConnectionGenes.append(innovationNumber)

	def addNode(self, connectionKey, innovationNumberIn = None, innovationNumberOut = None):
		self.connectionGenes[connectionKey].enabled = False
		newNode = NodeGene(self.nextNodeKey, 'HIDDEN', config.hiddenNodeActivation)
		self.nodeGenes[newNode.nodeNumber] = newNode

		if innovationNumberIn is None:
			innovationNumberIn = config.GlobalInnovationCounter
		self.addConnection(
			self.connectionGenes[connectionKey].inNodeKey,
			newNode.nodeNumber,
			self.connectionGenes[connectionKey].weight,
			True,
			innovationNumberIn
		)
		config.GlobalInnovationCounter += 1

		if innovationNumberOut is None:
			innovationNumberOut = config.GlobalInnovationCounter
		self.addConnection(
			newNode.nodeNumber,
			self.connectionGenes[connectionKey].outNodeKey,
			1.0,
			True,
			innovationNumberOut
		)
		config.GlobalInnovationCounter += 1

		self.nextNodeKey += 1

	@classmethod
	def crossover(cls, genome1, genome2):
		if genome1.fitness < genome2.fitness:
			genome1, genome2 = genome2, genome1
		genome = deepcopy(genome1)
		genome.fitness = None
		genome.species = None
		for key in genome1.connectionGenes:
			# Common genes are inherited from both parents
			if key in genome2.connectionGenes:
				genome.connectionGenes[key].weight = random.choice(
					[genome1.connectionGenes[key].weight,
					 genome2.connectionGenes[key].weight]
				)
				genome.connectionGenes[key].enabled = True
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

		# Shuffle to prevent only lower absolute value keys being preferred
		random.shuffle(inKeys)
		random.shuffle(outKeys)
		for inNodeKey in inKeys:
			for outNodeKey in outKeys:
				# Conditions here make sure that forward propagating connections are evolved only
				valid = inNodeKey != outNodeKey and self.nodeGenes[inNodeKey].nodeType != 'OUTPUT' and self.nodeGenes[outNodeKey].nodeType != 'INPUT'
				cyclic = self.isCyclic(inNodeKey, outNodeKey)
				alreadyExists = False
				for connection in self.connectionGenes:
					if self.connectionGenes[connection].inNodeKey == inNodeKey and self.connectionGenes[connection].outNodeKey == outNodeKey:
						alreadyExists = True
						break

				if valid and not cyclic and not alreadyExists:
					innovationNumber = None
					# Check whether this mutation has already occurred in this generation
					for mutation in connectionMutations:
						if inNodeKey == mutation.inNodeKey and outNodeKey == mutation.outNodeKey:
							innovationNumber = mutation.innovationNumber_s
					if innovationNumber is None:
						innovationNumber = config.GlobalInnovationCounter
						config.GlobalInnovationCounter += 1
						connectionMutations.append(Mutation(inNodeKey = inNodeKey, outNodeKey = outNodeKey, innovationNumber_s = innovationNumber))
					self.addConnection(
						inNodeKey,
						outNodeKey,
						(random.random() * 2) - 1,
						True,
						innovationNumber
					)
					return

		# If all possible connections exist then the network is fully connected
		self.fullyConnected = True

	def mutateAddNode(self, nodeMutations):
		connectionKey = None
		keys = [k for k in self.connectionGenes]
		random.shuffle(keys)
		for key in keys:
			if self.connectionGenes[key].enabled:
				connectionKey = key
				break

		# Sanity check
		if connectionKey is None:
			self.printDetails()
			raise ValueError('All connections of network are disabled!')

		# If mutation already happened then innovation numbers remain same of resulting connection genes
		innovationNumberIn, innovationNumberOut = None, None
		for mutation in nodeMutations:
			if mutation.inNodeKey == self.connectionGenes[connectionKey].inNodeKey and mutation.outNodeKey == self.connectionGenes[connectionKey].outNodeKey:
				innovationNumberIn, innovationNumberOut = mutation.innovationNumber_s[0], mutation.innovationNumber_s[1]

		# New mutation added in Node Mutations
		if innovationNumberIn is None and innovationNumberOut is None:
			nodeMutations.append(Mutation(inNodeKey = self.connectionGenes[connectionKey].inNodeKey, outNodeKey = self.connectionGenes[connectionKey].outNodeKey, innovationNumber_s = [config.GlobalInnovationCounter, config.GlobalInnovationCounter + 1]))

		# Finally adding the node
		self.addNode(connectionKey, innovationNumberIn = innovationNumberIn, innovationNumberOut = innovationNumberOut)

	def mutateChangeWeight(self):
		for connection in self.connectionGenes:
			if self.connectionGenes[connection].enabled and random.random() < 0.3:
				nudge = (random.random() - 0.5) * 0.1
				self.connectionGenes[connection].weight += nudge

	def mutateEnableConnection(self):
		keys = self.connectionGenes
		random.shuffle(keys)
		for key in keys:
			if not self.connectionGenes[key].enabled:
				self.connectionGenes[key].enabled = True
				return
		return

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

	# TODO: (CLEAN) Do something for this ugly visualisation function please
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
