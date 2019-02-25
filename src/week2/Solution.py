from collections import namedtuple
from typing import List, Any, Tuple

import matplotlib.colors
import numpy as np
from PIL import Image

import common.math.combinatorics as combinatorics
from common.math import pi
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
        res = {}
        repeat = 100
        for time in (1,10,100,1000,10000, 100000, int(1e6)):
            res[f'lei{time}'] = sampling.sample(lambda: pi.leibniz_formula(time), repeat)
            res[f'arch{time}'] = sampling.sample(lambda: pi.archimedes_sequence(time), repeat)
            res[f'monte{time}'] = sampling.sample(lambda: pi.monte_carlo(time), repeat)
        return '\n'.join(f'{k}: {v}' for k, v in res.items())


SOLUTIONS: List[Base] = [PartA(), PartB(), PartC()]
