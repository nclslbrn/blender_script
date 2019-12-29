from random import uniform, randint
from math import cos, sin, acos,  pi


class Agent:

    def __init__(self, size, x, y, z):

        self.x = x
        self.y = y
        self.z = z
        self.size = size
        self.stop = False

    def setSize(self, size):
        self.size = size

    def onLimit(self, limit, size):
        min = limit * -0.4
        max = limit * 0.4
        randSide = randint(0, 6)
        if randSide == 0:
            self.x = min
            self.y = uniform(min, max)
            self.z = uniform(min, max)
        elif randSide == 1:
            self.x = max
            self.y = uniform(min, max)
            self.z = uniform(min, max)
        elif randSide == 2:
            self.x = uniform(min, max)
            self.y = min
            self.z = uniform(min, max)
        elif randSide == 3:
            self.x = uniform(min, max)
            self.y = max
            self.z = uniform(min, max)
        elif randSide == 4:
            self.x = uniform(min, max)
            self.y = uniform(min, max)
            self.z = min
        else:
            self.x = uniform(min, max)
            self.y = uniform(min, max)
            self.z = max

        self.size = size
        self.stop = False

    def onRadius(self, limit, size):
        radius = limit * 0.95
        theta = uniform(0, 1) * pi * 2
        phi = acos(1 - uniform(0, 1) * 2)

        self.x = sin(phi) * cos(theta) * radius
        self.y = sin(phi) * sin(theta) * radius
        self.z = cos(phi) * radius
        self.size = size
        self.stop = False

    def move(self):
        if not self.stop:
            axe = randint(0, 5)
            if axe == 0:
                self.x += self.size
            elif axe == 1:
                self.y -= self.size
            elif axe == 2:
                self.y += self.size
            elif axe == 3:
                self.x -= self.size
            elif axe == 4:
                self.z += self.size
            elif axe == 5:
                self.z -= self.size

    def reInitIfOutside(self, limit):
        if (
            abs(self.x) > limit and
            abs(self.y) > limit and
            abs(self.z) > limit
        ):
            self.onRadius(limit, self.size)
