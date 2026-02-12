import matplotlib.pyplot as plt
import numpy as np
import copy

import k_mean as km
import knn
from sklearn.cluster import DBSCAN
# Code inspired from https://www.geeksforgeeks.org/machine-learning/k-means-clustering-introduction/

# Iterations
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
#x = array_np[:, 0]
#y = array_np[:, 1]
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

cluster_history[k+1] = copy.deepcopy(clusters)


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
for label in np.unique(labels): # Only the different states
    # Create a mask to filter just the correct points
    mask = labels == label
    plt.scatter(X[mask, 0], X[mask, 1], c=color_map[label], marker='x', label=label, zorder=1)

cluster_arrays = [[] for _ in range(len(clusters))]

# Plot cluster predictions for each iteration
for i ,clusters_ in cluster_history.items():

    for j, cluster in clusters_.items():
        # Simplify cluster to just (x, y) points
        cluster_arrays[j].append(cluster["center"])

for cluster in cluster_arrays:
    X = np.array([p[:2] for p in cluster], dtype=float)
    plt.plot(X[:, 0], X[:, 1], "*:", c="grey", zorder=2)
    #print(X)

# Highlight the end clusters
X = np.array([p["center"][:2] for p in clusters.values()], dtype=float)
plt.scatter(X[:,0], X[:,1], marker="*", c="orange", s=150, label="Clusters", zorder=3)

# Draw a mesh in the background to show the area of influence for each cluster
range_xy = (17, 19)
xx, yy = np.meshgrid(np.linspace(0, range_xy[0], 200), np.linspace(0, range_xy[1], 200))
grid = np.c_[xx.ravel(), yy.ravel()]

prediction = []
for point in grid:
    _, i, _ = km.predict(point, clusters)
    prediction.append(i)

Z = np.array(prediction, dtype=int).reshape(xx.shape)
plt.contourf(xx, yy, Z, alpha=0.2, zorder=0)

# Shows the plot
plt.xlabel("X1")
plt.ylabel("X2")
plt.title("K-means")
plt.grid(True)
plt.legend()
plt.show()

# Show the Pending chances for each cluster
print("=== K-mean ===")
for i, chance in km.chances(array, clusters).items():
    print(f"{i}: Cluster (X:{clusters[i]["center"][0]:0.2f}, Y:{clusters[i]["center"][1]:0.2f}), Pending {(chance.get("Pending", 0.0)*100.0):0.2f}%")

# Show the Pending chances for the knn calculation
print("=== KNN ===")
for i, j in enumerate(centroids):
    chance = knn.chances(j, array, k, offset=1)
    print(
        f"{i}: Point (X:{j[0]:0.2f}, Y:{j[1]:0.2f}), Pending {(chance.get("Pending", 0.0) * 100.0):0.2f}%")

# Show DBScan (Sadly using sklearn)
print("=== DBScan ===")
eps = 1.5
min_pts = 4

X = np.array([(p[0], p[1]) for p in array], dtype=float)

db = DBSCAN(eps=eps, min_samples=min_pts)
labels = db.fit_predict(X)

core_idx = db.core_sample_indices_          # indices of core points
core_mask = np.zeros(len(X), dtype=bool)
core_mask[core_idx] = True

# Report core points
print(f"DBSCAN parameters: eps={eps}, MinPts(min_samples)={min_pts}")
print(f"Number of core points: {core_mask.sum()}")
print("Core points (index -> (x1, x2)):")
for i in core_idx:
    print(f"  {i+1:2d} -> ({X[i,0]:.1f}, {X[i,1]:.1f})")  # +1 to match t = 1..33

# Cluster/noise summary
n_noise = np.sum(labels == -1)
clusters = sorted(set(labels) - {-1})
print("\nCluster summary:")
print(f"Number of clusters (excluding noise): {len(clusters)}")
print(f"Number of noise points: {n_noise}")

for c in clusters:
    members = np.where(labels == c)[0]
    print(f"  Cluster {c}: size={len(members)}")