import matplotlib.pyplot as plt
import matplotlib as mpl

import numpy as np

import a_star_algorithm as a_star

WIDTH = 6
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

path = a_star.a_star_search(MAP, WIDTH, start, goal)
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

cmap = mpl.colors.ListedColormap(["white", "green", "red"])
bounds = [2, 10]
norm = mpl.colors.BoundaryNorm(bounds, cmap.N, extend='both')

plt.imshow(arr, cmap=cmap, norm=norm)
plt.colorbar()

plt.axes().
ax.set_xticks(np.arange(0, 10, 1))
ax.set_yticks(np.arange(0, 10, 1))

# Labels for major ticks
ax.set_xticklabels(np.arange(1, 11, 1))
ax.set_yticklabels(np.arange(1, 11, 1))

#plt.axes().set_aspect('equal')
#plt.xticks([])
#plt.yticks([])
plt.show()



