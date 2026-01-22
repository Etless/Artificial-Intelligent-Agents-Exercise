import math

import numpy as np
from matplotlib import pyplot as plt

import genetic_algorithm as ga


# Random "unknown" function
def f(x):
    return math.sin(x) + 0.5 * math.cos(2*x) + 2

history, population = ga.iterate(50, 50, 0, 30, f, 0.5, 0.25)

# Final best
best_x = max(population, key=lambda x: f(x))
print("Best solution found:")
print("x =", best_x, "f(x) =", f(best_x))