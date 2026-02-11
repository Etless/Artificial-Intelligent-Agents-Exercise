import math


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

        if len(points) == 0:
            continue

        x = 0
        y = 0

        for point in points:
            x += point[0]
            y += point[1]

        size = len(points)
        cluster["center"] = [x/size, y/size]
        cluster["points"] = []


