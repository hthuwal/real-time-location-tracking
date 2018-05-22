import numpy as np
import math


def euclidean_distance(a, b):
    """Calculate the euclidean distance between vectors a and b."""
    a = np.array(a)
    b = np.array(b)
    return np.linalg.norm(a - b)


def root_mean_square_error(validation, test):
    """RMSQ error."""
    error = []
    for time in validation:
        if time in test:
            error.append(euclidean_distance(validation[time], test[time]))

    error = [e * e for e in error]
    length = len(error)
    return math.sqrt(sum(error) / length)
