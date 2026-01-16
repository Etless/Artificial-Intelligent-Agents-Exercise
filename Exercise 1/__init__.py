from sys import path_importer_cache

import matplotlib.pyplot as plt
import matplotlib as mpl

import numpy as np

import a_star_algorithm as a_star

"""WIDTH = 6
MAP = [1, 1, 2, 2, 1, 1,
       1, 1, 1, 1, 1, 1,
       1, 1, 1, 1, 1, 1,
       1, 1,10,10, 2, 1,
       1, 1, 1, 2, 2, 1,
       1, 1, 1, 1, 1, 1,
       1, 2,10,10, 1, 1,
       1, 1, 1, 1, 1, 1,
       1,10, 1, 1, 1, 1,]

start = (1, 0)
goal  = (4, 7)

path = a_star.a_star_search(MAP, WIDTH, start, goal, h=a_star.Diagonal)
print(path)

# Using code form Edgar Ramirez from stackoverflow
# https://stackoverflow.com/questions/53161342/plotting-a-maze-diagram-using-matplot-in-python

img2d = []
for j in range(len(MAP) // WIDTH):
       row = []
       for i in range(WIDTH):
              row.append(0 if MAP[i + j * WIDTH] == 1 else 1)#MAP[j * WIDTH + i])
       img2d.append(row)

arr = np.array(MAP)
arr = np.reshape(arr, (len(MAP) // WIDTH, WIDTH))

# Adds the correct colors to the correct values
cmap = mpl.colors.ListedColormap(["white", "green", "red"])
bounds = [2, 10]
norm = mpl.colors.BoundaryNorm(bounds, cmap.N, extend='both')

fig, ax = plt.subplots(figsize=(6, 6), dpi=100)
# Plot image of grid
ax.imshow(arr, cmap=cmap, norm=norm, interpolation="none", aspect="equal")

# Adds minor grid lines inbetween each cell
ax.set_xticks(np.arange(-0.5, arr.shape[1], 1), minor=True)
ax.set_yticks(np.arange(-0.5, arr.shape[0], 1), minor=True)
ax.grid(which="minor")
ax.tick_params(which="minor", bottom=False, left=False) # Hides the minor tick marks

# Create chosen path
path_np = np.array(path)

plt.plot(path_np[:, 0], path_np[:, 1], color="blue", linewidth=3, marker="o", markersize=6)
#plt.scatter(start[1], start[0], c="cyan", s=120, edgecolors="cyan", label="Start")
#plt.scatter(goal[1], goal[0], c="yellow", s=120, edgecolors="yellow", label="Goal")

#plt.colorbar()

#plt.axes().set_xticks(np.arange(0, 10, 1))
#plt.axes().set_yticks(np.arange(0, 10, 1))

# Labels for major ticks
#ax.set_xticklabels(np.arange(1, 11, 1))
#ax.set_yticklabels(np.arange(1, 11, 1))

#plt.axes().set_aspect('equal')
#plt.xticks([])
#plt.yticks([])
plt.show()"""

### ### GRID MAP ### ###
GRID = np.array([
       [1, 1, 2, 2, 1, 1,],
       [1, 1, 1, 1, 1, 1,],
       [1, 1, 1, 1, 1, 1,],
       [1, 1,10,10, 2, 1,],
       [1, 1, 1, 2, 2, 1,],
       [1, 1, 1, 1, 1, 1,],
       [1, 2,10,10, 1, 1,],
       [1, 1, 1, 1, 1, 1,],
       [1,10, 1, 1, 1, 1,]
])

start = (1, 0)
goal  = (4, 7)

path = a_star.test(GRID, start, goal, algorithm=a_star.Diagonal, iterations=1000000)

# Adds the correct colors to the correct values
cmap = mpl.colors.ListedColormap(["white", "green", "red"])
bounds = [2, 10]
norm = mpl.colors.BoundaryNorm(bounds, cmap.N, extend='both')

fig, ax = plt.subplots(figsize=(6, 6), dpi=100)
# Plot image of grid
ax.imshow(GRID, cmap=cmap, norm=norm, interpolation="none", aspect="equal")

# Adds minor grid lines inbetween each cell
ax.set_xticks(np.arange(-0.5, GRID.shape[1], 1), minor=True)
ax.set_yticks(np.arange(-0.5, GRID.shape[0], 1), minor=True)
ax.grid(which="minor")
ax.tick_params(which="minor", bottom=False, left=False) # Hides the minor tick marks

# Create chosen path
path_np = np.array(path)
plt.plot(path_np[:, 0], path_np[:, 1], color="blue", linewidth=3, marker="o", markersize=6)

plt.show()



