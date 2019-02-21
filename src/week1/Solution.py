import bisect
import math
from collections import defaultdict
from typing import List

import numpy as np
import svgwrite
import svgwrite.gradients
import svgwrite.shapes
from PIL import Image

from src.Base import Base


def divisor_count(n):
    divs = 0
    for i in range(int(math.sqrt(n))):
        i += 1
        if n % i == 0:
            divs += 1
    divs = 2 * divs - (1 if int(math.sqrt(n)) ** 2 == n else 0)
    return divs


class Collatz:
    def __init__(self):
        self.mem = {1: [1]}

    def get(self, n):
        if n in self.mem:
            return self.mem[n]
        nxt = (n // 2) if n % 2 == 0 else (n * 3 + 1)
        self.mem[n] = [n] + self.get(nxt)
        return self.mem[n]


class PartA(Base):

    def name(self):
        return 'A'

    def run(self, fnprovider):
        return '\n'.join(
            ['{}: {}'.format(n + 1, s) for n, s in enumerate([self.a1(), self.a2(), self.a3(), self.a4(), self.a5()])])

    def a1(self, n=10000):
        mx = [0, []]
        for i in range(1, n):
            dc = divisor_count(i)
            if dc > mx[0]:
                mx = [dc, [i]]
            elif dc == mx:
                mx[1].append(i)
        return '{} ({} divisors)'.format(', '.join(map(str, mx[1])), mx[0])

    def a2(self, top=1000, k=3):
        assert k > 0
        squares = {i * i: {(i,)} for i in range(1, int(math.sqrt(top)) + 1) if i * i < top}
        prev = squares
        for count in range(1, k):
            new = defaultdict(set)
            for anum, aitems in prev.items():
                for bnum, bitems in squares.items():
                    if anum + bnum < top:
                        for i in aitems:
                            for j in bitems:
                                new[anum + bnum].add(tuple(sorted(i + j)))
            prev = new

        return '{} numbers (smaller than {}) can not be written as a sum of {} squares'.format(
            top - 1 - len(prev), top, k)

    def a3(self, limit=10000):
        collatz = Collatz()
        mx = (-1, 0)
        for i in range(1, limit):
            steps = len(collatz.get(i))
            if mx[0] < steps:
                mx = (steps, i)
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


def isprime(n):
    for i in range(1, int(math.sqrt(n))):
        i += 1
        if n % i == 0:
            return False
    return True


def genprimes():
    n = 2
    while True:
        while not isprime(n):
            n += 1
        yield n
        n += 1


def add_tuple(t1, t2):
    return tuple(map(sum, zip(t1, t2)))


def mult_tuple(t1, t2):
    return tuple([a * b for a, b in zip(t1, t2)])


def corner(drawing: svgwrite.drawing.Drawing, size: int = 100, steps=10, pos=(0, 0), direction=(1, 1)):
    transform = lambda x: add_tuple(pos, mult_tuple(direction, x))
    for i in range(steps + 1):
        p = size / steps * i

        drawing.add(svgwrite.shapes.Line(transform((p, 0)), transform((size, p)), stroke='black'))


def star(drawing: svgwrite.drawing.Drawing, steps=10, pos=(0, 0)):
    corner(drawing, pos=add_tuple(pos, (0, 100)), direction=(1, 1), steps=steps)
    corner(drawing, pos=add_tuple(pos, (200, 100)), direction=(-1, 1), steps=steps)
    corner(drawing, pos=add_tuple(pos, (0, 100)), direction=(1, -1), steps=steps)
    corner(drawing, pos=add_tuple(pos, (200, 100)), direction=(-1, -1), steps=steps)


def inverse_star(drawing: svgwrite.drawing.Drawing, steps=10, pos=(0, 0)):
    corner(drawing, pos=add_tuple(pos, (100, 0)), direction=(1, 1), steps=steps)
    corner(drawing, pos=add_tuple(pos, (100, 0)), direction=(-1, 1), steps=steps)

    corner(drawing, pos=add_tuple(pos, (100, 200)), direction=(1, -1), steps=steps)
    corner(drawing, pos=add_tuple(pos, (100, 200)), direction=(-1, -1), steps=steps)


def calculate_color(x, y, ):
    print('x', x, 'y', y, )
    return


class PartB(Base):
    def name(self):
        return 'B'

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
        star(drawing, pos=(0, 0))
        star(drawing, pos=(200, 0), steps=30)
        inverse_star(drawing, pos=(0, 200))
        inverse_star(drawing, pos=(200, 200), steps=30)
        drawing.save()
        return ', '.join(fns)


def create_ulam(size):
    RIGHT = (0, 1)
    LEFT = (0, -1)
    UP = (-1, 0)
    DOWN = (1, 0)
    right = {RIGHT: UP, UP: LEFT, LEFT: DOWN, DOWN: RIGHT}
    array = np.zeros((2 * size + 1, 2 * size + 1), dtype=np.uint32)
    array[size][size] = 1
    pos = (size, size + 1)
    direction = UP
    value = 2
    for i in range(4 * size):
        while array[add_tuple(right[direction], pos)] != 0:
            array[pos] = value
            value += 1
            pos = add_tuple(pos, direction)
            if pos[0] == array.shape[0] or pos[1] == array.shape[1]:
                break
        direction = right[direction]
    return array


class Fib:
    def __init__(self):
        self.data = [1, 1]

    def goto(self, n):
        while self.data[-1] < n:
            self.data.append(self.data[-1] + self.data[-2])

    def __contains__(self, item):
        self.goto(item)
        res = bisect.bisect_left(self.data, item)
        return res != len(self.data) and self.data[res] == item


def trace(x, y, size, primes, delta):
    pos = (x, y)
    n = 0
    while size > pos[0] >= 0 and size > pos[1] >= 0:
        if primes[pos] == 0:
            break
        n += 1
        pos = add_tuple(pos, delta)
    return n


class PartC(Base):
    def name(self):
        return 'C'

    def run(self, fnprovider):
        fns = {}
        size = 500
        ulam = create_ulam(size)

        primes = np.uint8(np.vectorize(isprime)(ulam))
        fn = fnprovider.get_filename('.png', 'prime')
        fns['Primes'] = fn
        Image.fromarray(primes * 255, 'L').save(fn)

        traces = np.zeros((2,)+primes.shape, dtype=np.uint8)
        dim= 2*size+1
        for x in range(dim):
            for y in range(dim):
                traces[0][x][y] = trace(x, y, dim, primes, (1, 1)) + trace(x, y, dim, primes, (-1, -1)) - (1 if primes[x][y] else 0)
                traces[1][x][y] = trace(x, y, dim, primes, (-1, 1)) + trace(x, y, dim, primes, (1, -1)) - (1 if primes[x][y] else 0)
        threshold = 3
        d1 = traces[0] > threshold
        d2 = traces[1] > threshold
        lines = np.dstack((np.uint8(d2) * 255, np.zeros(primes.shape, dtype=np.uint8), np.uint8(d1) * 255))
        fn = fnprovider.get_filename('.png', 'lines')
        fns['Lines'] = fn
        Image.fromarray(lines, 'RGB').save(fn)

        fn = fnprovider.get_filename('.png', 'div5')
        fns['Div 5'] = fn
        Image.fromarray(np.uint8(np.vectorize(lambda n: n % 5 == 0)(ulam)) * 255, 'L').save(fn)

        fn = fnprovider.get_filename('.png', 'div8')
        fns['Div 8'] = fn
        Image.fromarray(np.uint8(np.vectorize(lambda n: n % 5 == 0)(ulam)) * 255, 'L').save(fn)

        fib = Fib()

        fn = fnprovider.get_filename('.png', 'fib')
        fns['Fib'] = fn
        Image.fromarray(np.uint8(np.vectorize(fib.__contains__)(ulam)) * 255, 'L').save(fn)

        return ', '.join('{}: {}'.format(i, j) for i, j in fns.items())


def gcd_mod(a, b):
    count = 0
    while True:
        if a < b:
            a, b = b, a
        if b == 0:
            return count
        a, b = b, a % b
        count += 1


def gcd_sub(a, b):
    count = 0
    while True:
        if a < b:
            a, b = b, a
        if a == b:
            return count
        a, b = a - b, b
        count += 1
    pass


class PartD(Base):
    def name(self):
        return 'D'

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
        stepsmod = np.fromfunction(lambda x, y: np.vectorize(gcd_mod)(x + 1, y + 1), shape=(size, size),
                                   dtype=np.uint32)
        stepsmod_n = stepsmod * 255 / np.max(stepsmod)
        Image.fromarray(np.uint8(stepsmod_n), 'L').save(fn)

        fn = fnprovider.get_filename('.png', 'gcdsub')
        fns['GCD sub time'] = fn
        stepssub = np.fromfunction(lambda x, y: np.vectorize(gcd_sub)(x + 1, y + 1), shape=(size, size),
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
