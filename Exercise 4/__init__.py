import math

import numpy as np
from matplotlib import pyplot as plt

import genetic_algorithm as ga


# Random "unknown" function
def f(x):
    return math.sin(x) + 0.5 * math.cos(2*x) + 2

# Data for the genetic algorithm
size = 50           # Population
generations = 1000000    # Iterations
min_pop = 0         # Range for initial x-values
max_pop = 30        # ^^^
mutation = 0.5      # Prob
crossover = 0.25    # ^^^

history, population = ga.iterate(size, generations, min_pop, max_pop, f, mutation, crossover)

# Final best
best_x = max(population, key=lambda x: f(x))
print("Best solution found:")
print("x =", best_x, "f(x) =", f(best_x))