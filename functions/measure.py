import numpy


def measure(first, second):

    a = numpy.array([first.x, first.y, first.z])
    b = numpy.array([second.x, second.y, second.z])

    return numpy.linalg.norm(a - b)
