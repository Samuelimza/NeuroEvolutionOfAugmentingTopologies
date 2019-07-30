# NeuroEvolutionOfAugmentingTopologies
NEAT (NeuroEvolution of Augmenting Topologies) is a method developed by Kenneth O. Stanley for evolving arbitrary neural networks.
This project is a Python implementation of NEAT.
You can find the original paper [here](http://nn.cs.utexas.edu/downloads/papers/stanley.ec02.pdf).

## Requirements
* [Python 3.6](https://www.python.org/downloads/release/python-360/) - Tested for python 3.6

## Installation
[Temporary - Adds a command to your .bashrc script that configures the $PYTOHNPATH path variable for you]

```
$ git clone https://github.com/Samuelimza/NeuroEvolutionOfAugmentingTopologies.git
$ cd NeuroEvolutionOfAugmentingTopologies
$ echo "export PYTHONPATH="\${PYTHONPATH}:$(pwd)"" >> ~/.bashrc
$ source ~/.bashrc
```
Run tests -

`$ python -m unittest discover -s tests`

or simply `$ ./runTests.sh`

## Usage
NEAT requires only a `fitness_function(Neural_Networks)` that evaluates neural networks and returns the fitness in a list as shown below:

```python
import neat

def fitness_function(Neural_Networks):
    fitness = []
    for neural_network in Neural_Networks:
        output = neural_network.activate(input_data)
        # Calculate fitness
        fitness.append(calculated_fitness)
    return fitness

NEAT_instance = neat.Main.NEAT(fitness_function)
NEAT_instance.train()
```

## Author
Osama Azmi - [github](https://github.com/Samuelimza)

## Contribute
Open issues if you discover any bugs or for feedback and contributors are always welcome!

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details 