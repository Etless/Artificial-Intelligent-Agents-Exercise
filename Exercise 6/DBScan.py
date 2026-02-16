import math

import numpy as np


def distance(point1, point2):
    return math.sqrt((point1.x - point2.x)**2 + (point1.y - point2.y)**2)

def get_cores(points):
    cores = []
    for point in points:
        if point.core:
            cores.append(point)

    cores.sort(key=lambda x: x.cluster)

    return cores

class Point:
    def __init__(self, x, y, state):
        self.x = x
        self.y = y
        self.state = state

        self.cluster = 0 # -1: Noise
        self.core = False
        self.visited = False

def assign(array, epsilon, min_pts):
    # Create points from array
    point_list = [Point(i, j, k) for i, j, k in array]
    cluster_id = 0

    for point in point_list:
        # Check if point is visited (processed)
        if point.visited:
            continue

        cluster = tree(point, point_list, epsilon, min_pts, cluster_id)
        cluster_id += 1 if cluster == cluster_id else 0
        point.visited = True

    return point_list
    """cores = []
    for point in point_list:
        index = 0
        for j, k in enumerate(array):
            if point.x == k[0] and point.y == k[1]:
                index = j
                break

        if not point.visited:
            print("ERROR")
        if point.core:
            print(f"{index} -> ({point.x}, {point.y})")
        cores.append(point.cluster)

    unique, counts = np.unique(np.array(cores, dtype=int), return_counts=True)
    return unique, counts"""



def tree(point, point_list, epsilon, min_pts, cluster_id):
    # Get all distances from point
    distance_list = [(distance(point, point_list[i]), i) for i in range(len(point_list))]
    distance_list.sort()

    # Remove points outside epsilon and itself from distances
    for i in range(len(distance_list)):
        if distance_list[i][0] > epsilon:
            distance_list = distance_list[0:i]
            break

    #print(len(distance_list))

    if len(distance_list) >= min_pts:  # Core point
        point.cluster = cluster_id
        point.core = True
        point.visited = True

        for _, i in distance_list:
            point_ = point_list[i]
            if point_.visited and not point_.cluster == -1:
                continue

            point_.visited = True
            point_.cluster = cluster_id

            tree(point_, point_list, epsilon, min_pts, cluster_id)

    elif not point.visited:
        point.cluster = -1

    return point.cluster

def predict(p, cores, epsilon):
    point = Point(p[0], p[1], "")

    distances = [(distance(point, core), core.cluster) for core in cores]
    distances.sort()

    # Remove cores outside epsilon
    for i in range(len(distances)):
        if distances[i][0] > epsilon:
            distances = distances[0:i]
            break

    if len(distances) == 0:
        return -1

    j = distances[0][1]
    if not all(i[1] == j for i in distances):
        return -2

    return distances[0][1]
