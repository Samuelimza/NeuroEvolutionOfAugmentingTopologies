import sys, os

# Make sure that the application source directory (this directory's parent) is
# on sys.path.

here = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, here)

import neat
print(dir(neat))
neatHello = neat.Main.NEAT(2)
print(neatHello.population[0].nodeGenes[0].nodeType)
