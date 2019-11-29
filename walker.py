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

    def SS(self):
        self.y += step

    def WW(self):
        self.x -= step
        return self

    def EE(self):
        self.x += step

    def NE(self):
        self.x += step * cos(quarterPi)
        self.y -= step * sin(quarterPi)

    def NW(self):
        self.x -= step * cos(quarterPi)
        self.y -= step * sin(quarterPi)

    def SE(self):
        self.x += step * cos(quarterPi)
        self.y += step * sin(quarterPi)

    def SW(self):
        self.x -= step * cos(quarterPi)
        self.y += step * sin(quarterPi)

    def UU(self):
        self.z += step

    def DD(self):
        self.z -= step

    moves = {
        'moveNN': NN,
        'moveNE': NE,
        'moveEE': EE,
        'moveSE': SE,
        'moveSS': SS,
        'moveSW': SW,
        'moveWW': WW,
        'moveNW': NW,
        'moveUU': UU,
        'moveDD': DD
    }

    def move(self):
        choosenMove = choice(list(self.moves.keys()))
        newPos = self.moves[choosenMove](self)
        return [self.x, self.y, self.z]


    
