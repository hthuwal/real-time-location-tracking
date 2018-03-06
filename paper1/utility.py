import math
from shapely.geometry import Point, Polygon
from shapely.ops import cascaded_union
from itertools import combinations
from scipy.optimize import fmin_tnc
import numpy as np


aps = {
    1: (-22, 1),
    2: (0, 1),
    3: (0, 24),
    4: (-22, 26)
}


def heuristic_3(circles):
    x, y = 0, 0
    t = 0
    for c in circles:
        w = 1.0 / (c[1])
        x += c[0][0] * w
        y += c[0][1] * w
        t += w

    return Point(x / t, y / t)


def fs(z, *args):
    x = z[0]
    y = z[1]
    cids = args[0]
    powers = args[1]
    params = args[2]

    F = 0
    for cid, p in zip(cids, powers):
        x0, y0 = aps[cid]
        hc = math.sqrt((x - x0)**2 + (y - y0)**2) * 39.3701 / 34
        F += (params[cid][0] - p - 10 * params[cid][1] * np.log10(hc))**2

    jac = np.zeros([2, ])
    for cid, p in zip(cids, powers):
        x0, y0 = aps[cid]
        hc = math.sqrt((x - x0)**2 + (y - y0)**2) * 39.3701 / 34
        jac[0] += (2 * (params[cid][0] - p - 10 * params[cid][1] * np.log10(hc)) * 10 * params[cid][1] * (x0 - x)) / (hc * hc)
        jac[1] += (2 * (params[cid][0] - p - 10 * params[cid][1] * np.log10(hc)) * 10 * params[cid][1] * (y0 - y)) / (hc * hc)

    jac[0] /= F
    jac[1] /= F
    return np.log(F), jac


def optimum(cids, powers, params, zinit):
    z = fmin_tnc(fs, list(zinit), args=(cids, powers, params))
    print(z[0])
    return z[0]


def rssi_to_dis(signal, p0, epsi):
    return (10**((p0 - signal) / (10 * epsi))) * (39.3701 / 34)


def rssi_to_dis_2(signal):
    n = 3
    return (10 ** ((-40 - signal) / (10 * n))) * (39.3701 / 34)


def root_mean_square_error(validation, test):
    error = []
    for time in validation:
        if time in test:
            p1 = Point(validation[time][0], validation[time][1])
            p2 = Point(test[time][0], test[time][1])
            error.append(p1.distance(p2))

    error = [e * e for e in error]
    l = len(error)
    return math.sqrt(sum(error) / l)
