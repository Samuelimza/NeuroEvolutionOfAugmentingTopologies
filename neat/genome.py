from copy import deepcopy
from . import config
from .utilityClasses import NodeGene, ConnectionGene, Mutation


class Genome:
	random = config.random

	def __init__(self):
		self.nextNodeKey = None
		self.nodeGenes = self.createNodeGenes()
		self.connectionGenes = self.createConnectionGenes()
		self.species = None
		self.fitness = None
		self.originalFitness = None
		self.fullyConnected = True

	def createDuplicateChild(self):
		"""
		Takes a genome and returns a copy with fitness and species cleared
		"""
		copied = deepcopy(self)
		copied.fitness = None
		copied.originalFitness = None
		copied.species = None
		return copied

	def createNodeGenes(self):
		"""
		Creates a default node structure with configured Input and Output nodes.
		By convention Output nodes have negative keys starting from -1 and Input nodes
		have positive keys starting from 0.
		"""
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
		"""
		Creates connections connecting the default input and output nodes with connection
		key as the innovation number. Each connection supplying a particular node has it's
		key stored in that node so the nodes supplying that particular node can be traced and
		their value can be calculatd recursively by the neural network.
		"""
		connectionGenes = {}
		connectionKey = 0
		for outputNodeKey in range(-1, -(config.noOfOutputNodes + 1), -1):
			for inputNodeKey in range(config.noOfInputNodes):
				connectionGenes[connectionKey] = ConnectionGene(
					inputNodeKey,
					outputNodeKey,
					(Genome.random.random() * 2) - 1,  # Use random weight here
					True,
					connectionKey
				)
				self.nodeGenes[outputNodeKey].supplyingConnectionGenes.append(connectionKey)
				connectionKey += 1

		if config.GlobalInnovationCounter == 0:
			config.GlobalInnovationCounter = connectionKey
		return connectionGenes

	def addConnection(self, inNodeKey, outNodeKey, weight, enabled, innovationNumber):
		"""
		Adds a connection in the genome with params

		Parameters:
			inNodeKey: Node key of the originating node of the connection
			outNodeKey: Node key of the terminating node of the connection
			weight: The weight of the connection being added
			enabled: Bool value if the connection is enabled
			innovationNumber: Unique innovation ID of the connection
		"""
		self.connectionGenes[innovationNumber] = ConnectionGene(
			inNodeKey,
			outNodeKey,
			weight,
			enabled,
			innovationNumber
		)
		self.nodeGenes[outNodeKey].supplyingConnectionGenes.append(innovationNumber)

	def addNode(self, connectionKey, innovationNumberIn = None, innovationNumberOut = None):
		"""
		Adds a connection in the genome with params

		Parameters:
			innovationNumberIn: Innovation ID for the incoming connection from the node
			innovationNumberOut: Innovation ID for the outgoing connection from the node
			connectionKey: Connection Key of an existing connection in the genome to split and add node in place of.
		"""
		self.connectionGenes[connectionKey].enabled = False
		newNode = NodeGene(self.nextNodeKey, 'HIDDEN', config.hiddenNodeActivation)
		self.nodeGenes[newNode.nodeNumber] = newNode

		if innovationNumberIn is None:
			innovationNumberIn = config.GlobalInnovationCounter
			config.GlobalInnovationCounter += 1
		self.addConnection(
			self.connectionGenes[connectionKey].inNodeKey,
			newNode.nodeNumber,
			self.connectionGenes[connectionKey].weight,
			True,
			innovationNumberIn
		)

		if innovationNumberOut is None:
			innovationNumberOut = config.GlobalInnovationCounter
			config.GlobalInnovationCounter += 1
		self.addConnection(
			newNode.nodeNumber,
			self.connectionGenes[connectionKey].outNodeKey,
			1.0,
			True,
			innovationNumberOut
		)

		self.nextNodeKey += 1

	@staticmethod
	def crossover(genome1, genome2):
		"""
		Returns a child resulted from the crossover of genomes passed

		Parameters:
			genome1: First parent
			genome2: Second parent
		 Returns:
		 	genome: Child
		"""
		if genome1.fitness < genome2.fitness:
			genome1, genome2 = genome2, genome1
		genome = genome1.createDuplicateChild()
		#for key in genome1.connectionGenes:
			# Common genes are inherited from both parents
		#	if key in genome2.connectionGenes:
		#		genome.connectionGenes[key].weight = Genome.random.choice(
		#			[genome1.connectionGenes[key].weight,
		#			 genome2.connectionGenes[key].weight]
		#		)
		return genome

	def mutate(self, connectionMutations, nodeMutations):
		"""
		Handles all mutations of a genome.

		Parameters:
			connectionMutations: List of connection mutations that have happened in the current generation
			nodeMutations: List of the node mutations that have happened in the current generation
		"""
		if config.mutateStructure and Genome.random.random() < config.mutateAddConnection and not self.fullyConnected:
			self.mutateAddConnection(connectionMutations)
		if config.mutateStructure and Genome.random.random() < config.mutateAddNode:
			self.mutateAddNode(nodeMutations)
		if Genome.random.random() < config.mutateWeights:
			self.mutateChangeWeight()
		if Genome.random.random() < config.mutateEnableGene:
			# self.mutateEnableConnection()
			pass

	def mutateAddConnection(self, connectionMutations):
		"""
		Adds a connection as a mutation in the genome

		Parameters:
			connectionMutations: The list of coonnection mutations occurred in the current generation
		"""
		inKeys = [k for k in self.nodeGenes.keys()]
		outKeys = [k for k in self.nodeGenes.keys()]

		# Shuffle to prevent only lower absolute value keys being preferred
		Genome.random.shuffle(inKeys)
		Genome.random.shuffle(outKeys)
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
						(Genome.random.random() * 2) - 1,
						True,
						innovationNumber
					)
					return

		# If all possible connections exist then the network is fully connected
		self.fullyConnected = True

	def mutateAddNode(self, nodeMutations):
		"""
		Adds a node as a mutation in the genome

		Parameters:
			nodeMutations: Node mutations occurred in the current generation
		"""
		connectionKey = None
		keys = [k for k in self.connectionGenes]
		Genome.random.shuffle(keys)
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
			innovationNumberIn = config.GlobalInnovationCounter
			config.GlobalInnovationCounter += 1
			innovationNumberOut = config.GlobalInnovationCounter
			config.GlobalInnovationCounter += 1
			nodeMutations.append(Mutation(inNodeKey = self.connectionGenes[connectionKey].inNodeKey, outNodeKey = self.connectionGenes[connectionKey].outNodeKey, innovationNumber_s = [innovationNumberIn, innovationNumberOut]))

		# Finally adding the node
		self.addNode(connectionKey, innovationNumberIn = innovationNumberIn, innovationNumberOut = innovationNumberOut)

		if self.fullyConnected:
			self.fullyConnected = False

	def mutateChangeWeight(self):
		"""
		Changes the connections' weights as a mutation
		"""
		for connection in self.connectionGenes:
			if self.connectionGenes[connection].enabled and Genome.random.random() < config.perturbationProbability:
				perturbationFactor = 1 + (((Genome.random.random() * 2) - 1) / 10)
				self.connectionGenes[connection].weight = self.connectionGenes[connection].weight * perturbationFactor
			else:
				self.connectionGenes[connection].weight = (Genome.random.random() * 2) - 1
		for node in self.nodeGenes:
			if Genome.random.random() < config.perturbationProbability:
				perturbationFactor = 1 + (((Genome.random.random() * 2) - 1) / 5)
				self.nodeGenes[node].bias = self.nodeGenes[node].bias * perturbationFactor
			else:
				self.nodeGenes[node].bias = (Genome.random.random() * 2) - 1

	def mutateEnableConnection(self):
		"""
		Enables a disabled connection as a mutation
		"""
		keys = self.connectionGenes
		Genome.random.shuffle(keys)
		for key in keys:
			if not self.connectionGenes[key].enabled:
				self.connectionGenes[key].enabled = True
				return
		return

	def isCyclic(self, inNodeKey, outNodeKey):
		"""
		Checks whether self would be cyclicly connected if inNodeKey and outNodeKey were to be connected by a connection.

		Parameters:
			inNodeKey: Input node for the connection to be added.
			outNodeKey: Output node for the connection to be added.
		Returns:
			bool: whether the connection makes the genome cyclic
		"""
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
		# Should this be inNodeKey or outNodeKey,or does it even matter??
		return dfs(inNodeKey, realStack)

	@staticmethod
	def genomeDistance(genome1, genome2):
		"""
		Returns the species distance between two genomes according to some speciation parameters.

		Parameters:
			genome1: First genome of the two.
			genome2: Second genome of the two.
		Returns:
			distance: The distance
		"""
		averageWeightDifference = 0
		noOfMatchingGenes = 0
		if len(genome1.connectionGenes) < len(genome2.connectionGenes):
			genome1, genome2 = genome2, genome1
		for gene in genome1.connectionGenes:
			if gene in genome2.connectionGenes:
				averageWeightDifference += abs(genome1.connectionGenes[gene].weight - genome2.connectionGenes[gene].weight)
				noOfMatchingGenes += 1
		disjointAndExcessGenes = len(genome1.connectionGenes) + len(genome2.connectionGenes) - 2 * noOfMatchingGenes
		averageWeightDifference = averageWeightDifference / noOfMatchingGenes
		distance = config.disjointAndExcessGeneFactor * disjointAndExcessGenes + config.weightDifferenceFactor * averageWeightDifference
		return distance

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
				print("\t", connectionKey, "CONNECTION_DISABLED:", self.connectionGenes[connectionKey].printDetails())
		print("Genome printed")
