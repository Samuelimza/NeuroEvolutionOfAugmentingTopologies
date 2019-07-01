class ConnectionGene():
	def __init__(self, inNodeKey, outNodeKey, weight, enabled, innovationNumber):
		self.inNodeKey = inNodeKey
		self.outNodeKey = outNodeKey
		self.weight = weight
		self.enabled = enabled
		self.innovationNumber = innovationNumber
		
	def printDetails(self):
		return "({0})>--[{1:.3f}]-->({2})".format(self.inNodeKey, self.weight, self.outNodeKey)
	
	@classmethod
	def copy(cls):
		return cls(self.inNodeKey, self.outNodeKey, self.weight, self.enabled, self.innovationNumber)

class NodeGene():
	def __init__(self, nodeNumber, nodeType, activationFunction):
		self.nodeNumber = nodeNumber
		self.nodeType = nodeType
		self.activationFunction = activationFunction
		self.supplyingConnectionGenes = []
		
	def printDetails(self):
		return "({})".format(self.nodeNumber)
	
	@classmethod
	def copy(cls):
		return cls(self.nodeNumber, self.nodeType, self.activationFunction)
