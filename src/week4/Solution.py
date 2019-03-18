from typing import List, Any

from Base import Base, AbstractFilenameProvider
from PIL import Image
import numpy as np
import math

from common.math.geometry import normalize
from src.common.python.tuples import *


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
        assert len(points) > 2
        img = Image.new("RGB", (imgsize, imgsize), (0xff, 0xff, 0xff))
        prev = points[-1]
        for point in points:
            delta = point[0] - prev[0], point[1] - prev[1]
            for t in range(steps):
                t /= steps
                img.putpixel((int(prev[0] + delta[0] * t), int(prev[1] + delta[1] * t)), (0, 0, 0))
            prev = point
        for i in range(len(points) - 2):
            v1 = np.array(points[i]) - np.array(points[i + 1])
            v2 = np.array(points[i + 2]) - np.array(points[i + 1])
            sign = v1[0] * v2[1] - v1[1] * v2[0]
            if sign != 0:
                break
        assert sign != 0
        direction = v1 + v2
        if sign > 0:
            direction = -1 * direction
        direction = normalize(direction) / 10
        i = 0
        while img.getpixel(tuple(direction * i + np.array(points[1]))) != (255, 255, 255):
            i += 1
        self.fill(img, direction * i + np.array(points[1]), (0, 0, 0))
        return img

    def fill(self, img, source, color):
        q = [np.array(source, dtype=np.int32)]
        while q:
            coords = q.pop()
            if img.getpixel(tuple(map(int, coords))) != color:
                img.putpixel(tuple(coords), color)
                for direction in map(np.array, [(1, 0), (-1, 0), (0, 1), (0, -1)]):
                    nc = coords + direction
                    if nc[0] < 0 or nc[1] < 0 or nc[0] >= img.width or nc[1] >= img.height:
                        continue
                    if nc != color:
                        q.append(nc)


class PartC(Base):
    name = 'C'

    def run(self, fnprovider: AbstractFilenameProvider):
        self.grid().save(fnprovider.get_filename('.png', 'grid', 'Grid'))
        self.circles().save(fnprovider.get_filename('.png', 'circles', 'Circles'))
        self.color_grid().save(fnprovider.get_filename('.png', 'color_grid', 'Color grid'))
        return fnprovider.format_files()

    def grid(self, size=100, step=10) -> Image.Image:
        img = Image.new('1', (size, size), color=1)
        for x in range(size):
            for y in range(size):
                if (x // step + y // step) % 2 == 1:
                    img.putpixel((x, y), 0)
        mask = Image.new('1', (size, size), color=0)
        for x in range(size):
            for y in range(size):
                x1 = x - size // 2
                y1 = y - size // 2
                if (math.sqrt(x1 ** 2 + y1 ** 2) // 22) % 2 == 1:
                    mask.putpixel((x, y), 1)
        self.apply_img(img, mask, lambda c: (c + 1) % 2)
        return img

    def apply_img(self, img: Image.Image, mask: Image.Image, fun: Callable[[Any], Any]):
        assert mask.width == img.width
        assert mask.height == img.height
        assert mask.mode == '1'
        for x in range(img.width):
            for y in range(img.height):
                if mask.getpixel((x, y)) == 1:
                    img.putpixel((x, y), fun(img.getpixel((x, y))))

    def circles(self, size=100, step=2):
        img = Image.new('L', (size, size), color=255)
        for x in range(size):
            for y in range(size):
                x1, y1 = x - size // 2, y - size // 2
                val = (math.sin(math.sqrt(x1 ** 2 + y1 ** 2) / step) + 1) / 2 * 256
                img.putpixel((x, y), int(val))
        mask = Image.new('1', (size, size), color=0)
        for x in range(size // 4, 3 * size // 4):
            for y in range(size // 4, 3 * size // 4):
                mask.putpixel((x, y), 1)
        self.apply_img(img, mask, lambda c: (255 - c) % 256)
        return img

    def color_grid(self, size=100):
        img = Image.new('RGB', (size, size), color=(0, 0, 0))
        for x in range(size):
            for y in range(size):
                r = (math.cos(x) + 1) / 2 * 256
                g = (math.cos(x + y) + 1) / 2 * 256
                b = (math.cos(y) + 1) / 2 * 256
                img.putpixel((x, y), tuple(map(int, (r, g, b))))
        return img


class PartD(Base):
    name = 'D'

    def run(self, fnprovider: AbstractFilenameProvider):
        self.s1('resources/w4/skryvacka1.png').save(
            fnprovider.get_filename('.png', 'skryvacka1', 'Skrývačka 1'))
        self.s2('resources/w4/skryvacka2.png').save(
            fnprovider.get_filename('.png', 'skryvacka2', 'Skrývačka 2'))
        self.s3('resources/w4/skryvacka3.png').save(
            fnprovider.get_filename('.png', 'skryvacka3', 'Skrývačka 3'))
        return fnprovider.format_files()

    def s1(self, fn):
        source: Image.Image = Image.open(fn)
        image = Image.new('1', source.size)
        for x in range(source.width):
            for y in range(source.height):
                image.putpixel((x, y), 1 if source.getpixel((x, y))[2] != 0 else 0)
        return image

    def s2(self, fn, maxdelta=15):
        source: Image.Image = Image.open(fn)
        image = Image.new('1', source.size)
        for x in range(source.width):
            for y in range(source.height):
                this = np.array(source.getpixel((x, y)))
                delta = 0
                for dx in (1, 0):
                    for dy in (1, 0):
                        if x + dx in range(image.width) and y + dy in range(image.height):
                            delta += np.sum(np.abs(np.array(source.getpixel((x + dx, y + dy))) - this))
                image.putpixel((x, y), 1 if delta < maxdelta else 0)
        return image

    def s3(self, fn):
        source: Image.Image = Image.open(fn)
        source = source.convert('1')
        image = Image.new('1', source.size)
        for x in range(source.width):
            for y in range(source.height):
                image.putpixel((x, y), ((x + y) % 2) ^ source.getpixel((x, y)))
        return image


SOLUTIONS: List[Base] = [PartA(), PartB(), PartC(), PartD()]
