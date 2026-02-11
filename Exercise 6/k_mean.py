import math

import numpy as np
from numpy.ma.core import append


def distance(point1, point2):
    return math.sqrt((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2)

def assign(array, clusters):
    for e in array:

        # Used to find the closest cluster
        min_distance = math.inf
        min_cluster = None

        for cluster in clusters.values():
            dist = distance(e, cluster["center"])
            if dist < min_distance:
                min_distance = dist
                min_cluster = cluster

        min_cluster["points"].append(e)


def update(array, clusters):
    for cluster in clusters.values():
        points = cluster["points"]

        # Makes sure there are elements connected to cluster
        if len(points) == 0:
            continue

        # Calculate average/mean of all points to cluster
        x = 0
        y = 0
        for point in points:
            x += point[0]
            y += point[1]

        size = len(points)
        cluster["center"] = [x/size, y/size] # New center is the average
        cluster["points"] = []


def predict(point, clusters):
    # Used to find the closest cluster
    min_distance = math.inf
    min_cluster = None
    min_index = -1

    for i, cluster in clusters.items():
        dist = distance(point, cluster["center"])
        if dist < min_distance:
            min_distance = dist
            min_cluster = cluster
            min_index = i

    return min_cluster, min_index, min_distance

def chances(array, clusters):

    for cluster in clusters.values():
        # Makes sure points are clear
        cluster["points"] = []

    # Assign points to clusters
    assign(array, clusters)

    # Calculate chances for each cluster
    cluster_chances = {}
    for i, cluster in clusters.items():
        # Makes sure there are elements connected to cluster
        if len(cluster["points"]) == 0:
            continue

        # We only care about states
        states_, count = np.unique([p[2] for p in cluster["points"]], return_counts=True)

        cluster_chances[i] = {}

        size = int(np.sum(count))
        count = count.astype(int).tolist()
        states_ = states_.astype(str).tolist()

        for j in range(len(states_)):
            cluster_chances[i][states_[j]] = count[j] / size

    return cluster_chances




