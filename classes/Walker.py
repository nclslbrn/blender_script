from math import sin, cos, pi
from random import choice

step = 0.5
quarterPi = pi / 4


class Walker:

    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    # MOOVE FUNCTIONS

    def NN(self):
        self.y -= step
        return self

    def SS(self):
        self.y += step
        return self

    def WW(self):
        self.x -= step
        return self

    def EE(self):
        self.x += step
        return self

    def NE(self):
        self.x += step * cos(quarterPi)
        self.y -= step * sin(quarterPi)
        return self

    def NW(self):
        self.x -= step * cos(quarterPi)
        self.y -= step * sin(quarterPi)
        return self

    def SE(self):
        self.x += step * cos(quarterPi)
        self.y += step * sin(quarterPi)
        return self

    def SW(self):
        self.x -= step * cos(quarterPi)
        self.y += step * sin(quarterPi)
        return self

    def UU(self):
        self.z += step
        return self
    
    def UW(self):
        self.x -= step * cos(quarterPi)
        self.z += step * sin(quarterPi)
        return self

    def UE(self):
        self.x += step * cos(quarterPi)
        self.z += step * sin(quarterPi)
        return self

    def UN(self):
        self.y += step * cos(quarterPi)
        self.z += step * sin(quarterPi)
        return self

    def US(self):
        self.y -= step * cos(quarterPi)
        self.z += step * sin(quarterPi)
        return self

    def DD(self):
        self.z -= step
        return self

    def DW(self):
        self.x -= step * cos(quarterPi)
        self.z -= step * sin(quarterPi)
        return self

    def DE(self):
        self.x += step * cos(quarterPi)
        self.z -= step * sin(quarterPi)
        return self

    def DN(self):
        self.y += step * cos(quarterPi)
        self.z -= step * sin(quarterPi)
        return self

    def DS(self):
        self.y -= step * cos(quarterPi)
        self.z -= step * sin(quarterPi)
        return self

    def move(self):
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
        choosenMove = choice(list(moves.keys()))
        newPos = moves[choosenMove]()
        self = newPos

        return self
