import gym
import neat
import numpy as np


env = gym.make('CartPole-v0')


def fitness_function(Neural_Networks):
	fitness = []
	for neural_network in Neural_Networks:
		individualFitness = 0
		observationa = env.reset()
		for t in range(1000):
			# env.render()
			inputs = np.array(observationa).reshape(1, 4)
			action = neural_network.activate(inputs)
			if action[0][0] < 0.5:
				action = 0
			else:
				action = 1
			observationa, reward, done, info = env.step(action)
			individualFitness += reward
			if done:
				print("Episode finished after {} timesteps".format(t + 1))
				break
		fitness.append(individualFitness)
	return fitness


neat.config.noOfInputNodes = 4
neat.config.noOfOutputNodes = 1
neat.config.totalGenerations = 10
neat.config.populationSize = 10
NEAT_instance = neat.Main.NEAT(fitness_function)
genomes = NEAT_instance.train()

# Test the elite of the generation for passing of the experiment
elite = NEAT_instance.convertToNeuralNetwork(genomes[0])
failed = False
for i in range(100):
	individualFitness = 0
	observationa = env.reset()
	for t in range(200):
		# env.render()
		inputs = np.array(observationa).reshape(1, 4)
		action = elite.activate(inputs)
		if action[0][0] < 0.5:
			action = 0
		else:
			action = 1
		observationa, reward, done, info = env.step(action)
		individualFitness += reward
		if done:
			# print("Episode finished after {} timesteps".format(t + 1))
			break
	if individualFitness < 195:
		failed = True
		break
if failed:
	print("Experiment failed")
else:
	print("Experiment passed")
	print("200 iterations balanced for greater than 195 timesteps!!")

env.close()
