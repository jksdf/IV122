import random


class Dice:
    def __init__(self, init):
        assert len(init) == 6
        init = list(init)
        s = sum(init)
        self.ranges = [0] * 7
        for i in range(1, 7):
            self.ranges[i] = self.ranges[i - 1] + init[i - 1] / s

    def roll(self):
        rand = random.random()
        for idx in range(6):
            if self.ranges[idx] <= rand < self.ranges[idx + 1]:
                return idx + 1
        assert False