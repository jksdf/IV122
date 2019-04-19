import random
import typing
from collections import Counter
from typing import Iterable

import matplotlib.pyplot as plt

from Base import Base, AbstractFilenameProvider
from week9.Dice import Dice

K_a = Dice(range(1, 7))
K_b = Dice(range(6, 0, -1))


def n_rolls(dice: Iterable[Dice], n) -> float:
    die = random.choice(dice)
    c = []
    for _ in range(n):
        c.append(die.roll())
    return sum(c) / len(c)


def samples(fn: typing.Callable[[int], float], n: int):
    avgs = []
    for _ in range(n):
        avgs.append(fn(random.choice([0, 1])))
    return avgs


def findpeaks(data, buckets):
    bucketed = [0] * len(buckets)
    for datapoint in data:
        for idx in range(len(buckets) - 1):
            if buckets[idx] <= datapoint < buckets[idx + 1]:
                bucketed[idx] += 1
                break
    peaks = []
    for idx in range(1, len(bucketed) - 1):
        if bucketed[idx - 1] < bucketed[idx] > bucketed[idx + 1]:
            peaks.append((buckets[idx] + buckets[idx+1])/2)
    return peaks


def drawResults(n, iters, prec=10):
    f, ax = plt.subplots(2, 2)
    buckets = [i / prec for i in range(6 * prec + 1)]

    ax[0][0].set_title("$K_a$ only")
    pos = samples(lambda _: n_rolls([K_a], n), iters)
    ax[0][0].hist(pos, buckets)
    for peak in findpeaks(pos, buckets):
        ax[0][0].axvline(x=peak, color='red')

    ax[0][1].set_title("$K_a$ and $K_b$ randomly")
    pos = samples(lambda _: n_rolls([K_a, K_b], n), iters)
    ax[0][1].hist(pos, buckets)
    for peak in findpeaks(pos, buckets):
        ax[0][1].axvline(x=peak, color='red')

    ax[1][0].set_title("$K_a$ and $K_b$ randomly for entire series")
    pos = samples(lambda x: n_rolls([[K_a, K_b][x]], n), iters)
    ax[1][0].hist(pos, buckets)
    for peak in findpeaks(pos, buckets):
        ax[1][0].axvline(x=peak, color='red')

    f.subplots_adjust(hspace=0.3)
    f.suptitle(f"Distributions with {n} iterations")
    return f


class PartC(Base):
    name = 'C'

    def run(self, fnprovider: AbstractFilenameProvider):
        plt.clf()
        random.seed(433308)
        iters = 100000
        drawResults(20, iters).savefig(fnprovider.get_filename(".png", "test_20", "Test 20"))
        drawResults(50, iters).savefig(fnprovider.get_filename(".png", "test_50", "Test 50"))
        drawResults(100, iters).savefig(fnprovider.get_filename(".png", "test_100", "Test 100"))
        return fnprovider.format_files()
