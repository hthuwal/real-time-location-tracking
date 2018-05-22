import math
from shapely.geometry import Point
from scipy.optimize import fmin
import numpy as np


aps = {
    1: (-22, 1),
    2: (0, 1),
    3: (0, 24),
    4: (-22, 26)
}


def length(v):
    """Length of a 2D vector."""
    return math.sqrt(v[0]**2 + v[1]**2)


def dot_product(v, w):
    """Dot Product of two 2D Vectors."""
    return v[0] * w[0] + v[1] * w[1]


def inner_angle(v, w):
    """Inner angle between two 2D vectors."""
    cosx = dot_product(v, w) / (length(v) * length(w))
    rad = math.acos(cosx)  # in radians
    return rad, cosx


def jitter_error(x, y, x1, y1, x2, y2):
    """
    Angle of deviation from original Path.

    Original Direction:
        x1,y1 -> x2,y2

    New Direction:
        x2,y2 -> x,y

    """
    return inner_angle([x - x2, y - y2], [x2 - x1, y2 - y1])


def dell_jitter_error(x, y, x1, y1, x2, y2):
    """
    Gradient of Angle of Deviaton from original path.

    May be needed by some optimization technique.
    """
    if (x1 == x2 and y1 == y2):
        return 0, 0
    c = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
    nr = (x - x2) * (x2 - x1) + (y - y2) * (y2 - y1)
    ans1 = (x2 - x1) / math.sqrt((x - x2)**2 + (y - y2)**2)
    ans1 -= (nr * (x - x2)) / (((x - x2)**2 + (y - y2)**2)**(1.5))
    ans1 *= (1 / c)

    ans2 = (x2 - x1) / math.sqrt((x - x2)**2 + (y - y2)**2)
    ans2 -= (nr * (x - x2)) / (((x - x2)**2 + (y - y2)**2)**(1.5))
    ans2 *= (1 / c)

    return ans1, ans2


def fs(z, *args):
    """f(x,y) to be optimized."""
    x, y = z
    cids, powers, params, x1, y1, x2, y2 = args

    F = 0
    # jitters = 0
    for cid, p in zip(cids, powers):
        x0, y0 = aps[cid]
        hc = math.sqrt((x - x0)**2 + (y - y0)**2) * 39.3701 / 34
        F += (params[cid][0] - p - 10 * params[cid][1] * np.log10(hc))**2

    return np.log(F)


def optimum(cids, powers, params, zinit, x1, y1, x2, y2):
    """Optimize f(x,y) using Downhill simplex algorthm."""
    z = fmin(fs, list(zinit), args=(cids, powers, params, x1, x2, y1, y2))
    return z


def rssi_to_dis(signal, p0, epsi):
    """
    Calculate distance based on signal strength.

    Arguments:
        signal -- Received Signal Strength
        p0 -- Signal Strength at 1 meter
        epsi -- epsilon

    Returns
        dstance -- distance in inches/tile

    """
    return (10**((p0 - signal) / (10 * epsi))) * (39.3701 / 34)


def root_mean_square_error(validation, test):
    """
    Give correct positions and Predicted Positions calculate the RMSQ error.

    Arguments:
        validation [dict: key-time, value-(x,y)] -- Correct Postitions
        test [dict: key-time, value-(x,y)] -- Predicted Postitions

    Returns:
        RMSQ error

    """
    error = []
    for time in validation:
        if time in test:
            p1 = Point(validation[time][0], validation[time][1])
            p2 = Point(test[time][0], test[time][1])
            error.append(p1.distance(p2))

    error = [e * e for e in error]
    l = len(error)
    return math.sqrt(sum(error) / l)
