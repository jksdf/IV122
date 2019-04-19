import random

import matplotlib.pyplot as plt

from Base import Base, AbstractFilenameProvider


class MontyHall:
    def __init__(self):
        self._state = [False] * 3
        self._state[random.randint(0, 2)] = True
        self.selected = None
        self.shown = None

    def select(self, pos):
        assert pos in range(3)
        self.selected = pos
        possible = [idx for idx, st in enumerate(self._state) if idx != pos and not st]
        self.shown = random.choice(possible)

    def swap(self, doSwap):
        assert self.selected is not None and self.shown is not None
        if doSwap:
            x = set(range(3))
            x.remove(self.selected)
            x.remove(self.shown)
            return self._state[list(x)[0]]
        else:
            return self._state[self.selected]

    def won(self):
        return self._state[self.selected]


def play(swapper, iter=1000000):
    wins = 0
    for _ in range(iter):
        monty_hall = MontyHall()
        monty_hall.select(random.randint(0, 2))
        if monty_hall.swap(swapper()):
            wins += 1
    return wins / iter


class PartA(Base):
    name = 'A'

    def run(self, fnprovider: AbstractFilenameProvider):
        plt.clf()
        fig, ax = plt.subplots()
        fig.suptitle("Monty hall distributions by strategy")
        ax.set_ylabel('Win rate')
        ax.set_xlabel('Strategy')
        ax.bar(list(range(3)), [play(lambda : True), play(lambda :False), play(lambda :random.choice([True, False]))], tick_label=['Always swap', 'Never swap', 'Random'])
        fig.savefig(fnprovider.get_filename('.png', 'monty_hall_distribution', 'Monty hall distributions by strategy'))
        return fnprovider.format_files()
