from collections import defaultdict
from typing import List, Dict, AbstractSet

import numpy as np
import svgwrite
import svgwrite.gradients
import svgwrite.shapes
from PIL import Image
from matplotlib import pyplot as plt

from common.math.Collatz import Collatz
from common.math.Fibonacci import Fibonacci
from common.math.factorization import *
from common.math.ulam import create_ulam
from common.python.tuples import *
from src.Base import Base


class PartA(Base):
    name = 'A'

    def run(self, fnprovider):
        return '\n'.join(
            ['{}: {}'.format(n + 1, s) for n, s in
             enumerate([self.a1(), self.a2(fnprovider), self.a3(), self.a4(), self.a5()])])

    def a1(self, n=10000):
        mx = [0, []]
        for i in range(1, n):
            dc = divisor_count(i)
            if dc > mx[0]:
                mx = [dc, [i]]
            elif dc == mx:
                mx[1].append(i)
        return '{} ({} divisors)'.format(', '.join(map(str, mx[1])), mx[0])

    def a2(self, fnprovider, top=1000, k=3):
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
        fn = fnprovider.get_filename(suffix='.png', name='sumsqdist')
        value, versions = zip(*prev.items())
        versions = list(map(len, versions))
        plt.clf()
        plt.bar(value, versions)
        plt.savefig(fn)
        return '{} numbers (smaller than {}) can not be written as a sum of {} squares, distribution in {}'.format(
            top - 1 - len(prev), top, k, fn)

    def a3(self, limit=10000):
        collatz = Collatz()
        mx = max((collatz.get(i), i) for i in range(1, limit))
        return '{} completes in {} steps'.format(mx[1], mx[0])

    def a4(self, limit=1000):
        sm = 0
        for p in genprimes():
            if p >= limit:
                break
            if '3' not in str(p):
                sm += p
        return str(sm)

    def a5(self, limit=1000000):
        seq = [1, 1]
        while seq[-1] <= limit:
            a, b = seq[-1], seq[-2]
            seq.append(a + b + math.gcd(a, b))
        return str(seq[-1])


class PartB(Base):
    name = 'B'

    def run(self, fnprovider):
        fns = []
        fn = fnprovider.get_filename('.png', 'raster')
        fns.append(fn)
        imgdim = 300
        imgsize = (imgdim, imgdim)
        image_array = np.dstack((np.fromfunction(lambda x, y: 256 * y / imgdim, shape=imgsize, dtype=np.uint32),
                                 np.zeros(shape=imgsize, dtype=np.uint32),
                                 np.fromfunction(lambda x, y: 256 * x / imgdim, shape=imgsize, dtype=np.uint32)))
        image = Image.fromarray(np.uint8(image_array))
        image.save(fn)

        fn = fnprovider.get_filename('.svg', 'star')
        fns.append(fn)
        drawing = svgwrite.Drawing(fn)
        self.star(drawing, pos=(0, 0))
        self.star(drawing, pos=(200, 0), steps=30)
        self.inverse_star(drawing, pos=(0, 200))
        self.small_inverse_square(drawing, pos=(250, 250))
        drawing.save()
        return ', '.join(fns)

    def corner(self, drawing: svgwrite.drawing.Drawing, size: int = 100, steps=10, pos=(0, 0), direction=(1, 1)):
        transform = lambda x: add_tuple(pos, mult_tuple(direction, x))
        for i in range(steps + 1):
            p = size / steps * i
            drawing.add(svgwrite.shapes.Line(transform((p, 0)), transform((size, p)), stroke='black'))

    def star(self, drawing: svgwrite.drawing.Drawing, steps=10, pos=(0, 0)):
        self.corner(drawing, pos=add_tuple(pos, (0, 100)), direction=(1, 1), steps=steps)
        self.corner(drawing, pos=add_tuple(pos, (200, 100)), direction=(-1, 1), steps=steps)
        self.corner(drawing, pos=add_tuple(pos, (0, 100)), direction=(1, -1), steps=steps)
        self.corner(drawing, pos=add_tuple(pos, (200, 100)), direction=(-1, -1), steps=steps)

    def inverse_star(self, drawing: svgwrite.drawing.Drawing, steps=10, pos=(0, 0)):
        self.corner(drawing, pos=add_tuple(pos, (100, 0)), direction=(1, 1), steps=steps)
        self.corner(drawing, pos=add_tuple(pos, (100, 0)), direction=(-1, 1), steps=steps)
        self.corner(drawing, pos=add_tuple(pos, (100, 200)), direction=(1, -1), steps=steps)
        self.corner(drawing, pos=add_tuple(pos, (100, 200)), direction=(-1, -1), steps=steps)

    def small_inverse_square(self, drawing: svgwrite.drawing.Drawing, steps=10, pos=(0, 0)):
        self.corner(drawing, pos=add_tuple(pos, (0, 0)), direction=(1, 1), steps=steps)
        self.corner(drawing, pos=add_tuple(pos, (100, 0)), direction=(-1, 1), steps=steps)
        self.corner(drawing, pos=add_tuple(pos, (100, 100)), direction=(-1, -1), steps=steps)
        self.corner(drawing, pos=add_tuple(pos, (0, 100)), direction=(1, -1), steps=steps)


class PartC(Base):
    name = 'C'

    def run(self, fnprovider):
        fns = {}
        size = 500
        ulam = create_ulam(size)

        fn = fnprovider.get_filename('.png', 'prime')
        fns['Primes'] = fn
        Image.fromarray(np.uint8(np.vectorize(isprime)(ulam)) * 255, 'L').save(fn)

        fn = fnprovider.get_filename('.png', 'div5')
        fns['Div 5'] = fn
        Image.fromarray(np.uint8(ulam % 5 == 0) * 255, 'L').save(fn)

        fn = fnprovider.get_filename('.png', 'div8')
        fns['Div 8'] = fn
        Image.fromarray(np.uint8(ulam % 8 == 0) * 255, 'L').save(fn)

        fib = Fibonacci()
        fn = fnprovider.get_filename('.png', 'fib')
        fns['Fib'] = fn
        Image.fromarray(np.uint8(np.vectorize(fib.__contains__)(ulam)) * 255, 'L').save(fn)

        return '\n'.join('{}: {}'.format(i, j) for i, j in fns.items())


class PartD(Base):
    name = 'D'

    def run(self, fnprovider):
        fns = {}

        size = 1500

        fn = fnprovider.get_filename('.png', 'pairwise')
        fns['Are pairwise divisible'] = fn
        Image.fromarray(
            np.fromfunction(lambda x, y: 255 * np.uint8(np.gcd(x + 1, y + 1) != 1), shape=(size, size),
                            dtype=np.uint32),
            'L').save(fn)

        fn = fnprovider.get_filename('.png', 'gcd')
        fns['GCD / MAX'] = fn
        Image.fromarray(
            np.fromfunction(lambda x, y: np.uint8(np.gcd(x + 1, y + 1) * 255 / np.maximum(x + 1, y + 1)),
                            shape=(size, size), dtype=np.uint32),
            'L').save(fn)

        fn = fnprovider.get_filename('.png', 'gcdmod')
        fns['GCD mod time'] = fn
        stepsmod: np.ndarray = np.fromfunction(lambda x, y: np.vectorize(gcd_mod)(x + 1, y + 1), shape=(size, size),
                                               dtype=np.uint32)
        stepsmod_n = stepsmod * 255 / np.max(stepsmod)
        Image.fromarray(np.uint8(stepsmod_n), 'L').save(fn)

        fn = fnprovider.get_filename('.png', 'gcdsub')
        fns['GCD sub time'] = fn
        stepssub: np.ndarray = np.fromfunction(lambda x, y: np.vectorize(gcd_sub)(x + 1, y + 1), shape=(size, size),
                                               dtype=np.uint32)
        stepssub_n = stepssub * 255 / np.max(stepssub)  # Normalize the step counts
        Image.fromarray(np.uint8(stepssub_n), 'L').save(fn)

        fn = fnprovider.get_filename('.png', 'gcdboth')
        fns['both GCD (blue = SUB, red = MOD) (log scale)'] = fn
        stepssub = np.log(stepssub)
        stepsmod = np.log(stepsmod)
        mx = max(np.max(stepssub), np.max(stepsmod))
        stepssub_n2 = np.uint8(stepssub * 255 / mx)
        stepsmod_n2 = np.uint8(stepsmod * 255 / mx)
        Image.fromarray(np.dstack((stepssub_n2, np.zeros((size, size), dtype=np.uint8), stepsmod_n2)), 'RGB').save(fn)

        return ',\n'.join('{}: {}'.format(i, j) for i, j in fns.items())


SOLUTIONS: List[Base] = [PartA(), PartB(), PartC(), PartD()]
