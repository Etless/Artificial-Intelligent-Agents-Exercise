from sys import path_importer_cache

import matplotlib.pyplot as plt
import matplotlib as mpl

import numpy as np

import a_star_algorithm as a_star
import depth_first_algorithm as depth

### ### GRID MAP ### ###
GRID = [
       [1, 1, 2, 2, 1, 1,],
       [1, 1, 1, 1, 1, 1,],
       [1, 1, 1, 1, 1, 1,],
       [1, 1,10,10, 2, 1,],
       [1, 1, 1, 2, 2, 1,],
       [1, 1, 1, 1, 1, 1,],
       [1, 2,10,10, 1, 1,],
       [1, 1, 1, 1, 1, 1,],
       [1,10, 1, 1, 1, 1,]
]

start = (1, 0)
goal  = (4, 7)

path_a, cost_a = a_star.search(GRID, start, goal, algorithm=a_star.Manhattan, iterations=0)
path_d, cost_d = depth.search(GRID, start, goal, algorithm=a_star.Manhattan, iterations=0)

print(cost_a, cost_d)

# Adds the correct colors to the correct values
cmap = mpl.colors.ListedColormap(["white", "green", "red"])
bounds = [2, 10]
norm = mpl.colors.BoundaryNorm(bounds, cmap.N, extend='both')

fig, ax = plt.subplots(figsize=(6, 6), dpi=100)
# Plot image of grid
ax.imshow(GRID, cmap=cmap, norm=norm, interpolation="none", aspect="equal", zorder=1)

# Adds minor grid lines inbetween each cell
ax.set_xticks(np.arange(-0.5, len(GRID[0]), 1), minor=True)
ax.set_yticks(np.arange(-0.5, len(GRID), 1), minor=True)
ax.grid(which="minor")
ax.tick_params(which="minor", bottom=False, left=False) # Hides the minor tick marks

# Create chosen path
if path_a is not None:
       path_np = np.array(path_a)
       ax.plot(path_np[:, 0], path_np[:, 1], color="blue", linewidth=3, marker="o", markersize=6, label="A*", zorder=2)

if path_d is not None:
       path_np = np.array(path_d)
       ax.plot(path_np[:, 0], path_np[:, 1], color="grey", linewidth=3, marker="o", markersize=6, label="DFS", zorder=2)


ax.scatter(start[0], start[1], c="cyan", s=120, edgecolors="cyan", label="Start", zorder=3)
ax.scatter(goal[0], goal[1], c="orange", s=120, edgecolors="orange", label="Goal", zorder=3)

ax.legend()

plt.title(
       f"A* Path – Total Cost = {cost_a:2d} \n"
       f"DFS Path – Total Cost = {cost_d:2d}"
)

plt.show()



