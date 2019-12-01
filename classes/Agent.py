from random import uniform, randint
from math import cos, sin, pi


class Agent:

    def __init__(self, size, x, y, z):

        self.x = x
        self.y = y
        self.z = z
        self.size = size
        self.stop = False

    def set(self, limit, speed, size):
        min = limit * -0.5
        max = limit * 0.5
        self.x = uniform(min, max)
        self.y = uniform(min, max)
        self.z = uniform(min, max)
        self.speed = speed
        self.size = size
        self.stop = False

        return self

    def onRadius(self, limit, speed, size):
        radius = limit / 2
        angle = uniform(0, pi * 2)
        self.x = radius * cos(angle)
        self.y = radius * sin(angle)
        self.z = radius * cos(angle)
        self.speed = speed
        self.size = size
        self.stop = False

        return self

    def move(self):

        if not self.stop:

            axe = randint(0, 5)

            if axe == 0:
                self.x += self.speed
            elif axe == 1:
                self.y -= self.speed
            elif axe == 2:
                self.y += self.speed
            elif axe == 3:
                self.x -= self.speed
            elif axe == 4:
                self.z += self.speed
            elif axe == 5:
                self.z -= self.speed

        return self
