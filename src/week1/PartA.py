import math
from collections import defaultdict
from typing import Dict, AbstractSet, Tuple

from matplotlib import pyplot as plt

from Base import Base
from common.math.Collatz import Collatz
from common.math.factorization import divisor_count, genprimes


def a1(n=10000):
    mx = [0, []]
    for i in range(1, n):
        dc = divisor_count(i)
        if dc > mx[0]:
            mx = [dc, [i]]
        elif dc == mx:
            mx[1].append(i)
    return '{} ({} divisors)'.format(', '.join(map(str, mx[1])), mx[0])


def a2(fnprovider, top=1000, k=3):
    assert k > 0
    squares: Dict[int, int] = {i * i: i for i in range(1, int(math.sqrt(top)) + 1) if i * i < top}
    prev: Dict[int, AbstractSet[Tuple[int, ...]]] = {key: {(value,)} for key, value in squares.items()}
    for count in range(1, k):
        new = defaultdict(set)
        for leftsum, tuples in prev.items():
            for square, base in squares.items():
                if leftsum + square < top:
                    for tup in tuples:
                        new[leftsum + square].add(tuple(sorted((base,) + tup)))
        prev = new
    fn = fnprovider.get_filename('.png', 'sumsqdist', 'Sum square distance')
    value, versions = zip(*prev.items())
    versions = list(map(len, versions))
    plt.clf()
    plt.bar(value, versions)
    plt.savefig(fn)
    return '{} numbers (smaller than {}) can not be written as a sum of {} squares'.format(top - 1 - len(prev), top, k)


def a3(limit=10000):
    collatz = Collatz()
    mx = max((collatz.get(i), i) for i in range(1, limit))
    return '{} completes in {} steps'.format(mx[1], mx[0])


def a4(limit=1000):
    sm = 0
    for p in genprimes():
        if p >= limit:
            break
        if '3' not in str(p):
            sm += p
    return str(sm)


def a5(limit=1000000):
    seq = [1, 1]
    while seq[-1] <= limit:
        a, b = seq[-1], seq[-2]
        seq.append(a + b + math.gcd(a, b))
    return str(seq[-1])


class PartA(Base):
    name = 'A'

    def run(self, fnprovider):
        return fnprovider.format_files(a1=a1(), a2=a2(fnprovider), a3=a3(), a4=a4(), a5=a5())
        #
        # ['{}: {}'.format(n + 1, s) for n, s in
        #  enumerate([a1(), a2(fnprovider), a3(), a4(), a5()])])
