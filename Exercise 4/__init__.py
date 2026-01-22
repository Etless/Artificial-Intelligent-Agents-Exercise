import math

import numpy as np
from matplotlib import pyplot as plt

import genetic_algorithm as ga


# Random "unknown" function
def f(x):
    return math.sin(x) + 0.5 * math.cos(2*x) + 2

# Data for the genetic algorithm
size = 50           # Population
generations = 50    # Iterations
min_pop = 0         # Range for initial x-values
max_pop = 30        # ^^^
mutation = 0.5      # Prob
crossover = 0.25    # ^^^

# Perform the genetic algorithm
history, population = ga.iterate(size, generations, min_pop, max_pop, f, mutation, crossover)

best_history = max(history, key=lambda x: f(x))
best_final = max(population, key=lambda x: f(x))

print(f"Best History: ({best_history:1.4f}, {f(best_history):1.4f}) :: Best Final: ({best_final:1.4f}, {f(best_final):1.4f})")



#vari = abs(best_final - best_history) // 10

min_x = min(min(history), min(population)) - 5
max_x = max(max(history), max(population)) + 5

# Plot the function and place point of the
# final and best value
x_vals = np.linspace(min_x, max_x, 400)
y_vals = [f(x) for x in x_vals]
plt.plot(x_vals, y_vals, label="f(x)")

points_x = history
points_y = [f(x) for x in points_x]

plt.plot(points_x, points_y, 'o', label="Points")

plt.title(f"Best value = {f(best_history):1.4f}")

#plt.legend()
plt.show()