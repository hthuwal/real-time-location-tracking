import math
from shapely.geometry import Point
from itertools import combinations


def fi(circles):
    """
    Find Intersection of circles.

    1. Centroid of Intersection of intersection of all pair of circles
    2. Centroid of intersction with min area among of intersection of all
    pair of circles
    3. None

    Arguments:
        circles -- list of ((x_center, y_center), radius)

    Returns:
        if 1 then 1 else if 2 then 2 else 3

    """
    cs = [Point(c[0][0], c[0][1]).buffer(c[1]) for c in circles]
    intersections = [a.intersection(b) for a, b in combinations(cs, 2)]

    intersection = []
    for each in intersections:
        if each.area != 0:
            intersection.append(each)

    ans = cs[0]
    for c in cs:
        ans = ans.intersection(c)

    if(ans.area != 0):
        return ans.centroid

    if(len(intersection) != 0):
        return min(intersection, key=lambda x: x.area).centroid

    return None


def heuristic_1(circles):
    """
    Estimate location based on circles.

    Arguments:
        circles -- list of ((x_center, y_center), radius)

    Returns:
        Centroid of Intersection of intersection of all pair of circles

    """
    cs = [Point(c[0][0], c[0][1]).buffer(c[1]) for c in circles]
    ans = cs[0]
    for c in cs:
        ans = ans.intersection(c)

    if(ans.area != 0):
        return ans.centroid

    return None


def heuristic_2(circles):
    """
    Estimate location based on circles.

    Arguments:
        circles -- list of ((x_center, y_center), radius)

    Returns:
        c = Centroid of Intersection of intersection of all pair of circles
        if c exists then c
        else Weighted centroid of all intersections where weight = 1/(r1*r2)

    """
    cs = [Point(c[0][0], c[0][1]).buffer(c[1]) for c in circles]
    intersections = [a.intersection(b) for a, b in combinations(cs, 2)]
    weights = [1 / (a[1] * b[1]) for a, b in combinations(circles, 2)]

    centroids = []
    weight = []
    for i, w in zip(intersections, weights):
        if i.area != 0:
            centroids.append(i.centroid)
            weight.append(w)

    ans = cs[0]
    for c in cs:
        ans = ans.intersection(c)

    if(ans.area != 0):
        return ans.centroid

    if(len(centroids) != 0):
        x, y = 0, 0
        t = 0
        for c, w in zip(centroids, weight):
            x += c.x * w
            y += c.y * w
            t += w

        return Point(x / t, y / t)

    return None


def heuristic_3(circles):
    """
    Estimate location based on circles.

    Arguments:
        circles -- list of ((x_center, y_center), radius)

    Returns:
        weighted average of the centers of circles where
        weight = 1 / radius

    """
    x, y = 0, 0
    t = 0
    for c in circles:
        w = 1.0 / (c[1])
        x += c[0][0] * w
        y += c[0][1] * w
        t += w

    return Point(x / t, y / t)


# Using either of the two methods seems to give same results

def signal_strength_to_distance(signal, freq):
    """
    Calculate distance based on signal strength.

    Arguments:
        signal -- Received Signal Strength
        freq -- frequency of the signal

    Returns
        dstance -- distance in inches/tile

    """
    distance = 10 ** ((27.55 + abs(signal) -
                       (20 * math.log10(freq * 1000))) / 20.0)
    distance = distance * 39.3701  # converting into inches
    return distance / 34


def rssi_to_dis(signal):
    """
    Calculate distance based on signal strength.

    Arguments:
        signal -- Received Signal Strength

    Returns
        dstance -- distance in inches/tile

    """
    n = 3
    return (10 ** ((-40 - signal) / (10 * n))) * (39.3701 / 34)


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
    length_err = len(error)
    return math.sqrt(sum(error) / length_err)
