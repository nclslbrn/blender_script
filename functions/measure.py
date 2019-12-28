from math import sqrt, pow


def measure(first, second):

    locx = second.x - first.x
    locy = second.y - first.y
    locz = second.z - first.z

    distance = sqrt(pow(locx, 2) + pow(locy, 2) + pow(locz, 3) * 1.0)
    return distance
