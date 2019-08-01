import unittest
import neat
import random


class TestGenome(unittest.TestCase):
	def test_Initialisation(self):
		neat.config.noOfOutputNodes = 2
		neat.config.noOfInputNodes = 2
		neat.config.outputNodeActivation = 'sigmoid'
		random.seed(0)
		neat.config.random = random
		genome = neat.genome.Genome()
		self.assertEqual(len(genome.nodeGenes), 4)
		self.assertEqual(len(genome.connectionGenes), 4)
		self.assertAlmostEqual(sum([genome.connectionGenes[connectionGeneKey].weight for connectionGeneKey in genome.connectionGenes]), 0.56372917)
		self.assertEqual(genome.nextNodeKey, 2)

	def test_GenomeDistance(self):
		neat.config.noOfInputNodes = 2
		neat.config.noOfOutputNodes = 1
		neat.config.disjointAndExcessGeneFactor = 1.0
		neat.config.weightDifferenceFactor = 1.0
		random.seed(0)
		neat.config.random = random
		genome1 = neat.genome.Genome()
		random.seed(1)
		neat.config.random = random
		genome2 = neat.genome.Genome()
		self.assertAlmostEqual(neat.genome.Genome.genomeDistance(genome1, genome2), 0.79953694)
		genome1.addNode(connectionKey = 0, innovationNumberIn = 2, innovationNumberOut = 3)
		genome2.addNode(connectionKey = 0, innovationNumberIn = 2, innovationNumberOut = 3)
		self.assertAlmostEqual(neat.genome.Genome.genomeDistance(genome1, genome2), 0.75479727)
		genome1.addNode(connectionKey = 2, innovationNumberIn = 4, innovationNumberOut = 5)
		genome2.addNode(connectionKey = 3, innovationNumberIn = 6, innovationNumberOut = 7)
		self.assertAlmostEqual(neat.genome.Genome.genomeDistance(genome1, genome2), 4.75479727)
		genome1.addConnection(inNodeKey = 1, outNodeKey = 3, weight = 0.25, enabled = True, innovationNumber = 8)
		genome2.addConnection(inNodeKey = 1, outNodeKey = 3, weight = 0.75, enabled = True, innovationNumber = 8)
		self.assertAlmostEqual(neat.genome.Genome.genomeDistance(genome1, genome2), 4.70383781)
		genome1.addConnection(inNodeKey = 2, outNodeKey = -1, weight = 0.1, enabled = True, innovationNumber = 9)
		genome2.addConnection(inNodeKey = 1, outNodeKey = 2, weight = 0.9, enabled = True, innovationNumber = 10)
		self.assertAlmostEqual(neat.genome.Genome.genomeDistance(genome1, genome2), 6.70383781)


if __name__ == '__main__':
	unittest.main()
