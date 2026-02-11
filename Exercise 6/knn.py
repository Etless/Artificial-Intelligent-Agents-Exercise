import math

import numpy as np


def distance(point1, point2):
    return math.sqrt((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2)

def chances(point, array, k, offset=0):

    # Saving all distances in memory!
    # This is the lazy way that wastes a lot of RAM in larger datasets
    distances = [(distance(point, p), p) for p in array]
    distances.sort()

    # Offset is to help remove the staring point if
    # it is included in the dataset
    distances = distances[offset:k+offset]

    # We only care about states
    states_, count = np.unique([p[1][2] for p in distances], return_counts=True)
    chances_ = {}

    size = int(np.sum(count))
    count = count.astype(int).tolist()
    states_ = states_.astype(str).tolist()

    for j in range(len(states_)):
        chances_[states_[j]] = count[j] / size

    return chances_
