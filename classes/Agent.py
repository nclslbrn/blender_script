import random


class Agent:

    def __init__(self, x, y, z):

        self.x = x
        self.y = y
        self.z = z
        self.stop = False

    def set(self, limit, speed):
        min = limit * -0.5
        max = limit * 0.5
        self.x = random.uniform(min, max)
        self.y = random.uniform(min, max)
        self.z = random.uniform(min, max)
        self.speed = speed
        self.stop = False

        return self

    def move(self):

        if not self.stop:

            axe = random.randint(0, 5)

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
