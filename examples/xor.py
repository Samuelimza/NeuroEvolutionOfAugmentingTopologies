import os
import sys
# Make sure that the application source directory (this directory's parent) is on sys.path.
here = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, here)


import neat
import numpy as np


def fitnessFunc(neuralNetworks):
    fitness = []
    inputs = np.array([[0.0, 0.0],
                       [0.0, 1.0],
                       [1.0, 0.0],
                       [1.0, 1.0]]
                      )
    outputTrain = np.array([[0.0],
                            [1.0],
                            [1.0],
                            [0.0]]
                           )
    for nn in neuralNetworks:
        outputNN = nn.activate(inputs)
        individualFitness = 4.0 - np.sum(np.absolute(outputNN - outputTrain))
        if individualFitness > 2.95:
            print('High fitness network output: ', outputNN)
            print('Network: ')
            nn.genome.printDetails()
        fitness.append(individualFitness)
    return fitness


neatHello = neat.Main.NEAT(fitnessFunc)
genomesAfterTraining = neatHello.train()

for genome in genomesAfterTraining:
    # genome.printDetails()
    pass
