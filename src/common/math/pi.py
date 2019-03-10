import math
import random
import sys
import time


def leibniz_formula(precision=1e-5):
    pi = 0.
    delta = 999
    k = 0
    while delta > precision:
        delta = (4. if k % 2 == 0 else -4.) / (2 * k + 1)
        pi += delta
        k += 1
    return pi


def archimedes_sequence(precision=1e-5):
    n = 2
    dn = math.sqrt(2)
    delta = 999
    while delta > precision:
        d2n = math.sqrt(2 - 2 * math.sqrt(1 - dn ** 2 / 4))
        if d2n < 0.0000001:
            break
        delta = abs(d2n * 2 * n - dn * n)
        dn = d2n
        n *= 2
    return dn * n


def monte_carlo(precision=1e-5):
    shots = 0
    hits = 0
    delta = 999
    while delta > precision:
        prev = hits / shots * 4 if shots else 0
        for _ in range(1000):
            x, y = random.random(), random.random()
            if x * x + y * y < 1:
                hits += 1
            shots += 1
        delta = abs(prev - hits / shots * 4)
    return hits / shots * 4
