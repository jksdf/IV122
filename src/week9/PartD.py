import random
from typing import Dict

import matplotlib.pyplot as plt
import numpy as np

from Base import Base, AbstractFilenameProvider
from week9.Dice import Dice

NORMAL_DIE = Dice([1] * 6)
ALL_6 = Dice([0] * 5 + [6])


def do_throws(N, X):
    dice = [NORMAL_DIE] * (N - 1) + [ALL_6]
    rolls = []
    die = random.choice(dice)
    for _ in range(X):
        rolls.append(die.roll())
    return die, rolls


def sample(N, X, k) -> Dict[bool, int]:
    states = {False: 0, True: 0}
    for _ in range(k):
        die, rolls = do_throws(N, X)
        if rolls == [6] * X:
            states[die is ALL_6] += 1
    total = sum(states.values())
    for y in (True, False):
        states[y] /= total
    return states


class PartD(Base):
    name = 'D'

    def run(self, fnprovider: AbstractFilenameProvider):
        iters = 100000
        for N in (5, 10, 20, 50, 100):
            plt.clf()
            x = np.array(list(range(2, 10)))
            y2 = [sample(N, X, iters) for X in x]
            y = [v[True] for v in y2]
            z = [v[False] for v in y2]
            plt.bar(x, y, width=0.2, color='red')
            plt.bar(x, z, bottom=y, width=0.2, color='blue')
            plt.legend(['fake', 'correct'])
            plt.xlabel(f'Number of throws')
            plt.ylabel(f'Probability of the kind of die')
            plt.title(f'{N} dice')
            plt.savefig(fnprovider.get_filename('.png', f'samples_N{N}', f'Samples with N = {N}'))
        return fnprovider.format_files()
