import math
import random
import sys
import time


def leibniz_formula(dtime=None):
    pi = 0.
    k = 0
    target_time = time.thread_time_ns() + dtime
    while time.thread_time_ns() < target_time:
        pi += (4. if k % 2 == 0 else -4.) / (2 * k + 1)
        k += 1
    return pi


def archimedes_sequence(dtime=None):
    n = 2
    dn = math.sqrt(2)
    target_time = time.thread_time_ns() + dtime
    while time.thread_time_ns() < target_time:
        d2n = math.sqrt(2 - 2 * math.sqrt(1 - dn ** 2 / 4))
        if d2n < 0.0000001:
            break
        dn = d2n
        n *= 2
        # sys.stderr.write(f'{dn*n} ')
    return dn * n


def monte_carlo(dtime=None):
    shots = 0
    hits = 0
    target_time = time.thread_time_ns() + dtime
    while time.thread_time_ns() < target_time:
        x, y = random.random(), random.random()
        if x * x + y * y < 1:
            hits += 1
        shots += 1
    return hits / shots * 4
