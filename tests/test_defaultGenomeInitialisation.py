import unittest
import neat
import random


class TestDefaultGenomeInitialisations(unittest.TestCase):
	def test_Initialisation(self):
		"""
		Initialisation depends on:
			config.noOfInputNodes
			config.noOfOutputNodes
			config.outputNodeActivation
			random
		"""
		neat.config.noOfOutputNodes = 2
		neat.config.noOfInputNodes = 2
		neat.config.outputNodeActivation = 'sigmoid'
		genome = neat.genome.Genome(random = random)
		self.assertEqual(len(genome.nodeGenes), 4)
		self.assertEqual(len(genome.connectionGenes), 4)


if __name__ == '__main__':
	unittest.main()