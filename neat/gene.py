class ConnectionGene():
	def __init__(self, inNodeKey, outNodeKey, weight, enabled, innovationNumber):
		self.inNodeKey = inNodeKey
		self.outNodeKey = outNodeKey
		self.weight = weight
		self.enabled = enabled
		self.innovationNumber = innovationNumber

class NodeGene():
	def __init__(self, nodeNumber, nodeType, activationFunction):
		self.nodeNumber = nodeNumber
		self.nodeType = nodeType
		self.activationFunction = activationFunction
		self.supplyingConnectionGenes = []
