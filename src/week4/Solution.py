from typing import List

from Base import Base, AbstractFilenameProvider
from PIL import Image
import numpy as np
import math


class PartA(Base):
    name = 'A'

    def run(self, fnprovider: AbstractFilenameProvider):
        fns = {}

        fn = fnprovider.get_filename('.png', 'circle')
        self.circle(200, 80).save(fn)
        fns['Circle'] = fn

        fn = fnprovider.get_filename('.png', 'empty_circle')
        self.empty_circle(200, 80, 5).save(fn)
        fns['Empty circle'] = fn

        fn = fnprovider.get_filename('.png', 'gonio_circle')
        self.goniometric_circle(200, 80).save(fn)
        fns['Goniometric circle'] = fn

        fn = fnprovider.get_filename('.png', 'spiral')
        self.spiral(400, 160, 10).save(fn)
        fns['Spiral'] = fn

        fn = fnprovider.get_filename('.png', 'triangle')
        self.triangle(200).save(fn)
        fns['Triangle'] = fn

        fn = fnprovider.get_filename('.png', 'elipsis')
        self.elipsis(200, 80, 30).save(fn)
        fns['Elipsis'] = fn

        return '\n'.join(f'{k}: {v}' for k, v in fns.items())

    def circle(self, imgsize, radius):
        img = Image.new("RGB", (imgsize, imgsize), (0xff, 0xff, 0xff))
        for x in range(imgsize):
            for y in range(imgsize):
                if (x - imgsize // 2) ** 2 + (y - imgsize // 2) ** 2 <= radius ** 2:
                    img.putpixel((x, y), (0, 0, 0))
        return img

    def goniometric_circle(self, imgsize, radius, scale=1000):
        img = Image.new("RGB", (imgsize, imgsize), (0xff, 0xff, 0xff))
        for theta in range(int(math.pi * 2 * scale)):
            theta /= scale
            x = math.cos(theta) * radius
            y = math.sin(theta) * radius
            img.putpixel((int(x + imgsize // 2), int(y + imgsize // 2)), (0, 0, 0))
        return img

    def empty_circle(self, imgsize, radius, width):
        img = Image.new("RGB", (imgsize, imgsize), (0xff, 0xff, 0xff))
        for x in range(imgsize):
            for y in range(imgsize):
                if radius ** 2 >= (x - imgsize // 2) ** 2 + (y - imgsize // 2) ** 2 >= (radius - width) ** 2:
                    img.putpixel((x, y), (0, 0, 0))
        return img

    def spiral(self, imgsize, radius, turns, scale=1000):
        img = Image.new("RGB", (imgsize, imgsize), (0xff, 0xff, 0xff))
        for theta in range(int(2 * math.pi * scale * turns)):
            theta /= scale
            r = radius * theta / (2 * math.pi * turns)
            x = math.cos(theta) * r
            y = math.sin(theta) * r
            color = (int(abs(y) / (imgsize // 2) * 255), int(abs(x) / (imgsize // 2) * 255) if x < 0 else 0,
                     int(abs(x) / (imgsize // 2) * 255) if x > 0 else 0)
            img.putpixel((int(x + imgsize // 2), int(y + imgsize // 2)), color)
        return img

    def triangle(self, imgsize):
        img = Image.new("RGB", (imgsize, imgsize), (0xff, 0xff, 0xff))
        for x in range(imgsize):
            for y in range(imgsize):
                if y <= math.tan(math.pi / 3) * x and y <= -math.tan(math.pi / 3) * (x - imgsize):
                    color = (0, 0, 0)  # TODO: better colors
                    img.putpixel((imgsize - x - 1, imgsize - y - 1), color)
        return img

    def elipsis(self, imgsize, a, b):
        img = Image.new("RGB", (imgsize, imgsize), (0xff, 0xff, 0xff))
        for x in range(imgsize):
            for y in range(imgsize):
                val = ((x - imgsize // 2) / a) ** 2 + ((y - imgsize // 2) / b) ** 2
                if val <= 1:
                    img.putpixel((x, y), (int(255 * val), int(255 * val), int(255 * val)))
        return img


class PartB(Base):
    name = 'B'

    def run(self, fnprovider: AbstractFilenameProvider):
        fns = {}

        fn = fnprovider.get_filename('.png', 'polygon')
        self.polygon(200, [(10, 10), (180, 20), (160, 150), (100, 50), (20, 180)]).save(fn)
        fns['Polygon'] = fn
        return '\n'.join(f'{k}: {v}' for k, v in fns.items())

    def polygon(self, imgsize, points, steps=1000):
        img = Image.new("RGB", (imgsize, imgsize), (0xff, 0xff, 0xff))
        prev = points[-1]
        for point in points:
            delta = point[0] - prev[0], point[1] - prev[1]
            for t in range(steps):
                t /= steps
                img.putpixel((int(prev[0] + delta[0] * t), int(prev[1] + delta[1] * t)), (0, 0, 0))
            prev = point
        return img


SOLUTIONS: List[Base] = [PartA(), PartB()]
