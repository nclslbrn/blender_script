from math import sqrt


def measure(first, second):

    locx = second.x - first.x
    locy = second.y - first.y
    locz = second.z - first.z

    distance = sqrt((locx)**2 + (locy)**2 + (locz)**2)
    return distance
