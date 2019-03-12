import math
import time
from collections import namedtuple
from typing import List, Any, Tuple, Iterable

import matplotlib.colors
import numpy as np
from PIL import Image

import common.math.combinatorics as combinatorics
from common.math import pi, arithmetics
from common.python import sampling
from common.python.tuples import mult_tuple
from src.Base import Base, AbstractFilenameProvider


class PartA(Base):
    name = 'A'
    comb = namedtuple('Combinatorics',
                      ['permutations', 'combinations', 'combinations_repeated', 'variations', 'variations_repeated'])

    def run(self, fnprovider: AbstractFilenameProvider):
        t = self.combinatorics(3, [1, 2, 3, 4, 5])
        return 'permutations: {}\ncombinations: {}\ncombinations_repeated: {}\nvariations: {}\nvariations_repeated: {}'.format(
            t.permutations, t.combinations, t.combinations_repeated, t.variations, t.variations_repeated)

    def combinatorics(self, k: int, data: List[Any]) -> comb:
        return self.comb(combinatorics.permutations(data), combinatorics.combinations(k, data),
                         combinatorics.combinations_repeated(k, data), combinatorics.variations(k, data),
                         combinatorics.variations_repeated(k, data))


import matplotlib.pyplot


class PartB(Base):
    name = 'B'

    def run(self, fnprovider: AbstractFilenameProvider) -> str:
        fns = {}
        palette: List[Tuple[int, int, int]] = [tuple(map(int, mult_tuple(c, (255, 255, 255)))) for c in
                                               matplotlib.pyplot.get_cmap('Set3').colors]
        fn = fnprovider.get_filename(suffix='.png', name='pascal_50_5')
        fns['pascal_30_5'] = fn
        self.pascal_image(50, 5, palette[:5]).save(fn)
        fn = fnprovider.get_filename(suffix='.png', name='pascal_500_10')
        fns['pascal_500_10'] = fn
        self.pascal_image(500, 10, palette[:10]).save(fn)

        fn = fnprovider.get_filename(suffix='.png', name='pascal_500_5')
        fns['pascal_500_5'] = fn
        self.pascal_image(500, 5, palette[:5]).save(fn)

        return '\n'.join('{}: {}'.format(k, v) for k, v in fns.items())

    def pascal_image(self, n: int, d: int, palette: List[Tuple[int, int, int]]) -> Image.Image:
        assert len(palette) == d
        palette = list(map(np.array, palette))
        pascal = combinatorics.PascalTriangle(d)
        # each cell is 2x2
        array = np.full((2 * n, 2 * n, 3), 255, dtype=np.uint8)
        for r in range(n):
            for c in range(r + 1):
                value = pascal[r:c]
                color = palette[value]
                array[2 * r:2 * r + 2, n - r - 1 + 2 * c:n - r + 1 + 2 * c] = color
        img = Image.fromarray(array, mode='RGB')
        return img


class PartC(Base):
    name = 'C'

    def run(self, fnprovider: AbstractFilenameProvider):
        res = {'lei': {}, 'arch': {}, 'monte': {}}
        for time in range(3, 10):
            time = 10 ** time
            res['lei'][time] = sampling.sample(pi.leibniz_formula, time)
            res['arch'][time] = sampling.sample(pi.archimedes_sequence, time)
            res['monte'][time] = sampling.sample(pi.monte_carlo, time)
        labels = []
        for kind in res:
            keys, vals = zip(*res[kind].items())
            matplotlib.pyplot.loglog(keys, [abs(v - math.pi) / math.pi for v in vals])
            labels.append(kind)
        matplotlib.pyplot.legend(labels)
        matplotlib.pyplot.xlabel('Time')
        matplotlib.pyplot.ylabel('Runs')
        fn = fnprovider.get_filename(suffix='.png', name='pi_precision')
        matplotlib.pyplot.savefig(fn)
        matplotlib.pyplot.clf()
        return fn


class PartD(Base):
    name = 'D'

    def run(self, fnprovider: AbstractFilenameProvider):
        fn = fnprovider.get_filename('.png', 'pow_efficiency')
        self.efficiency_graph(fn, 123, (10 ** i for i in range(100)), 1000000007, trials=1000)
        return '\n'.join([self.get(123, 1234567, 1000000007),
                          self.get(9, 10, 2),
                          self.get(123456, 12345678901234567890, 1000000007, perform_inefficient=False),
                          f'efficiency graph {fn}'])

    def efficiency_graph(self, savefile, n, es: Iterable, m, trials=10):
        results = ([], [])
        for e in es:
            times = []
            for _ in range(trials):
                t0 = time.perf_counter_ns()
                arithmetics.pow(n, e, m)
                times.append(time.perf_counter_ns() - t0)
            results[0].append(e)
            results[1].append(sum(times) / len(times))
        matplotlib.pyplot.semilogx(*results)
        matplotlib.pyplot.savefig(savefile)
        matplotlib.pyplot.clf()

    def get(self, n, e, m, perform_inefficient=True):
        t = time.perf_counter_ns()
        p1 = arithmetics.pow(n, e, m)
        t1 = time.perf_counter_ns() - t
        if perform_inefficient:
            t = time.perf_counter_ns()
            p2 = arithmetics.pow_naive(n, e, m)
            t2 = time.perf_counter_ns() - t
            assert p1 == p2
        else:
            t2 = float('nan')
        return f'{n}^{e} (mod {m}) = {p1} ({t1} ns efficient, {t2} ns inefficient)'


SOLUTIONS: List[Base] = [PartA(), PartB(), PartC(), PartD()]
