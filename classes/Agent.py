from random import randint, uniform


class Agent:

    def __init__(self, x, y, z):

        self.x = x
        self.y = y
        self.z = z
        self.stop = False

    def set(self, limit, step):

        self.x = uniform(limit * -0.5, limit * 0.5)
        self.y = uniform(limit * -0.5, limit * 0.5)
        self.z = uniform(limit * -0.5, limit * 0.5)
        self.step = step
        self.stop = False

        return self

    def move(self):

        if not self.stop:

            axe = randint(0, 5)

            if axe == 0:
                self.x += self.step
            elif axe == 1:
                self.y -= self.step
            elif axe == 2:
                self.y += self.step
            elif axe == 3:
                self.x -= self.step
            elif axe == 4:
                self.z += self.step
            elif axe == 5:
                self.z -= self.step

            return self
