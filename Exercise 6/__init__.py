import matplotlib.pyplot as plt
import numpy as np
import copy

import k_mean as km
# Code inspired from https://www.geeksforgeeks.org/machine-learning/k-means-clustering-introduction/

k = 3

# x1 | x2 | Alarm state

array = (
    ( 7.5,  8.5, "Pending" ), ( 2.2,  7.3, "Pending" ), ( 3.2,  4.3, "Small"   ), #  1,  2,  3
    ( 4.2,  6.7, "Pending" ), ( 4.3,  5.8, "Small"   ), ( 4.5,  3.5, "Small"   ), #  4,  5,  6
    ( 2.2,  2.5, "Small"   ), ( 2.7,  3.7, "Small"   ), ( 4.5,  8.9, "Imminent"), #  7,  8,  9
    ( 8.5,  5.6, "Pending" ), ( 9.6,  4.6, "Pending" ), ( 7.5,  4.9, "Pending" ), # 10, 11, 12
    ( 4.5, 12.2, "Imminent"), ( 4.0, 13.5, "Imminent"), ( 8.6, 13.2, "Imminent"), # 13, 14, 15
    (10.2, 12.8, "Imminent"), (12.2, 17.8, "Imminent"), (13.5, 16.4, "Imminent"), # 16, 17, 18
    (15.6, 12.2, "Imminent"), (10.3, 10.4, "Pending" ), ( 9.8, 10.4, "Imminent"), # 19, 20, 21
    ( 8.3, 11.3, "Imminent"), ( 5.6,  7.8, "Imminent"), ( 7.8,  5.6, "Imminent"), # 22, 23, 24
    ( 4.7,  7.8, "Small"   ), ( 7.8,  4.6, "Pending" ), (13.3,  8.9, "Imminent"), # 25, 26, 27
    ( 3.4,  4.6, "Small"   ), ( 5.6,  6.6, "Small"   ), ( 7.9,  9.5, "Pending" ), # 28, 29, 30
    ( 5.8,  6.6, "Pending" ), ( 4.8,  4.6, "Pending" ), (12.4,  9.1, "Imminent")  # 31, 32, 33
)

array_np = np.array(array)

# Pick prototype form each state
x = array_np[:, 0]
y = array_np[:, 1]
centroids = [array[0][:2], array[2][:2], array[32][:2]] # Pending | Small | Imminent

# Cluster containing the closest points
clusters = {}
for i, centroid in enumerate(centroids):
    clusters[i] = {
        "center": centroid,
        "points": []
    }

cluster_history = {}

for i in range(k):
    km.assign(array, clusters)
    cluster_history[i] = copy.deepcopy(clusters)
    km.update(array, clusters)

cluster_history[k] = copy.deepcopy(clusters)
print(len(cluster_history))


# Color map to be used to filter/determine
# the color of each point
color_map = {
    "Small": "green",
    "Pending": "blue",
    "Imminent": "red"
}

# Convert points from array to numpy, and make them the
# correct type (defaults to object)
X = np.array([p[:2] for p in array], dtype=float)
labels = np.array([p[2] for p in array], dtype=str)

plt.figure()

# Draw all points on plot
for label in np.unique(labels):
    # Create a mask to filter just the correct points
    mask = labels == label
    plt.scatter(X[mask, 0], X[mask, 1], c=color_map[label], marker='x', label=label)

cluster_arrays = [[] for _ in range(len(clusters))]

# Plot cluster predictions for each iteration
for i ,clusters_ in cluster_history.items():

    for j, cluster in clusters_.items():
        # Simplify cluster to just (x, y) points
        cluster_arrays[j].append(cluster["center"])

for cluster in cluster_arrays:
    X = np.array([p[:2] for p in cluster], dtype=float)
    plt.plot(X[0], X[1], "*:", c="grey")
    #print(X)

X = np.array([p["center"][:2] for p in clusters.values()], dtype=float)
print(X)
plt.scatter(X[0], X[1], "*:", c="orange")

"""
# Draw plot
col = array_np[:, 2]
col = np.char.replace(col, "Small", "green")
col = np.char.replace(col, "Pending", "blue")
col = np.char.replace(col, "Imminent", "red")

xPoints = array_np[:, 0].astype(float)
yPoints = array_np[:, 1].astype(float)

plt.scatter(xPoints, yPoints, marker='x', c=col)

#plt.scatter(0,1)

for cluster in clusters.values():
    center = cluster["center"]
    plt.scatter(center[0], center[1], marker='*', c="black")

    print(center)

for i in cluster_history.values():
    for j in i.values():
        center = j["center"]
        plt.plot(center[0], center[1], '*', c="black")

#for i in range(len(array_np)):
#    plt.scatter(xPoints[i], yPoints[i], marker='x', c=col[i])
"""

plt.xlabel("X1")
plt.ylabel("X2")
plt.title("Array")
plt.grid(True)
plt.legend()
plt.show()