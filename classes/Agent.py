from random import uniform, randint
from math import cos, sin, pi


class Agent:

    def __init__(self, size, x, y, z):

        self.x = x
        self.y = y
        self.z = z
        self.size = size
        self.stop = False

    def set(self, limit, size):
        min = limit * -0.5
        max = limit * 0.5
        self.x = uniform(min, max)
        self.y = uniform(min, max)
        self.z = uniform(min, max)
        self.size = size
        self.stop = False

        return self

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
        return self

    def onRadius(self, limit, size):
        radius = limit / 2
        angle = uniform(0, pi * 2)
        self.x = radius * cos(angle)
        self.y = radius * sin(angle)
        self.z = radius * cos(angle)
        self.size = size
        self.stop = False

        return self

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

        return self

    def reinitIfOutside(self, limit):

        min = (limit) * -0.5
        max = (limit) * 0.5

        if(
            self.x < min or
            self.y < min or
            self.z < min or
            self.x > max or
            self.y > max or
            self.z > max
        ):
            self.onLimit(
                limit=limit,
                size=self.size
            )
