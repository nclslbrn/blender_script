from math import sin, cos, pi
from random import choice

quarterPi = pi / 4


class Walker:

    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
        self.size = 1

    def setSize(self, size):
        self.size = size

    # MOOVE FUNCTIONS
    def NN(self, distance):
        self.y -= distance
        return self

    def SS(self, distance):
        self.y += distance
        return self

    def WW(self, distance):
        self.x -= distance
        return self

    def EE(self, distance):
        self.x += distance
        return self

    def NE(self, distance):
        self.x += distance * cos(quarterPi)
        self.y -= distance * sin(quarterPi)
        return self

    def NW(self, distance):
        self.x -= distance * cos(quarterPi)
        self.y -= distance * sin(quarterPi)
        return self

    def SE(self, distance):
        self.x += distance * cos(quarterPi)
        self.y += distance * sin(quarterPi)
        return self

    def SW(self, distance):
        self.x -= distance * cos(quarterPi)
        self.y += distance * sin(quarterPi)
        return self

    def UU(self, distance):
        self.z += distance
        return self

    def UW(self, distance):
        self.x -= distance * cos(quarterPi)
        self.z += distance * sin(quarterPi)
        return self

    def UE(self, distance):
        self.x += distance * cos(quarterPi)
        self.z += distance * sin(quarterPi)
        return self

    def UN(self, distance):
        self.y += distance * cos(quarterPi)
        self.z += distance * sin(quarterPi)
        return self

    def US(self, distance):
        self.y -= distance * cos(quarterPi)
        self.z += distance * sin(quarterPi)
        return self

    def DD(self, distance):
        self.z -= distance
        return self

    def DW(self, distance):
        self.x -= distance * cos(quarterPi)
        self.z -= distance * sin(quarterPi)
        return self

    def DE(self, distance):
        self.x += distance * cos(quarterPi)
        self.z -= distance * sin(quarterPi)
        return self

    def DN(self, distance):
        self.y += distance * cos(quarterPi)
        self.z -= distance * sin(quarterPi)
        return self

    def DS(self, distance):
        self.y -= distance * cos(quarterPi)
        self.z -= distance * sin(quarterPi)
        return self

    def move(self, distance):
        moves = {
            'NN': self.NN,
            'NE': self.NE,
            'EE': self.EE,
            'SE': self.SE,
            'SS': self.SS,
            'SW': self.SW,
            'WW': self.WW,
            'NW': self.NW,
            'UU': self.UU,
            'UN': self.UN,
            'US': self.US,
            'UW': self.UW,
            'UE': self.UE,
            'DD': self.DD,
            'DW': self.DW,
            'DE': self.DE,
            'DN': self.DN,
            'DS': self.DS
        }
        distance += self.size/2
        choosenMove = choice(list(moves.keys()))
        newPos = moves[choosenMove](distance)
        self = newPos

        return self
