import random


class Pool:

    def __init__(self, maxItems):
        self.maxItems = maxItems
        self.items = []

    def update(self):
        self.items = []
        remaining = 1
        for a in range(self.maxItems):

            if(remaining > 0):
                item = random.uniform(0, a/self.maxItems) * remaining
                self.items.append(item)
                remaining -= item
            else:
                self.items.append(0)

    def getItems(self):
        return self.items
