import random
from numbers import Real
from typing import List, Tuple

import math

import svgwrite
import svgwrite.shapes

from src.Base import Base, AbstractFilenameProvider


class PartA(Base):
    name = 'A'

    def run(self, fnprovider: AbstractFilenameProvider):
        random.seed(433308)
        lines = self.gen_line_segments(500, 30, (0, 400))
        d = svgwrite.Drawing(fnprovider.get_filename('.svg', 'test', 'Test'))
        for start, end in lines:
            d.add(svgwrite.shapes.Line(start, end, stroke='black'))
        intersections = self.intersections(lines)
        for intersection in intersections:
            d.add(svgwrite.shapes.Circle(center=intersection, r=1, stroke='blue'))
        d.save()
        return fnprovider.format_files()

    def gen_line_segments(self, n, length, xy_range: Tuple[Real, Real]):
        lines = []
        for _ in range(n):
            x, y = random.uniform(*xy_range), random.uniform(*xy_range)
            angle = random.uniform(0, 2 * math.pi)
            lines.append(((x, y), (x + math.cos(angle) * length, y + math.sin(angle) * length)))
        return lines

    def intersections(self, lines: List[Tuple[Tuple[Real, Real], Tuple[Real, Real]]]) -> List[Tuple[Real, Real]]:
        intersections = []
        for i1 in range(len(lines)):
            for i2 in range(i1 + 1, len(lines)):
                l1, l2 = lines[i1], lines[i2]
                (x1, y1), (x2, y2) = l1
                (x3, y3), (x4, y4) = l2
                x = ((x1 * y2 - y1 * x2) * (x3 - x4) - (x1 - x2) * (x3 * y4 - y3 * x4)) / (
                    (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4))
                y = ((x1 * y2 - y1 * x2) * (y3 - y4) - (y1 - y2) * (x3 * y4 - y3 * x4)) / (
                    (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4))
                if min(x1, x2) <= x <= max(x1, x2) and min(x3, x4) <= x <= max(x3, x4) \
                        and min(y1, y2) <= y <= max(y1, y2) and min(y3, y4) <= y <= max(y3, y4):
                    intersections.append((x, y))
        return intersections


class PartB(Base):
    def run(self, fnprovider: AbstractFilenameProvider):
        points = self.gen_points(500, (0, 400))
        return fnprovider.format_files()

    def gen_points(self, n, xy_range):
        points = []
        for _ in range(n):
            points.append((random.uniform(*xy_range), random.uniform(*xy_range)))
        return points


class PartC(Base):
    def run(self, fnprovider: AbstractFilenameProvider):
        points = self.gen_points(500, (0, 400))

        return fnprovider.format_files()

    def jarvis(self, points):
        left = points[0]
        for p in points:
            left = min(left, p)
        verts = [left]
        while len(verts) <= 1 or verts[0] != verts[0]:
            for v in points:
                if v != verts[-1]:
                    dist = math.sqrt((verts[-1][0] - v[0]) ** 2 + (verts[-1][1] - v[1]) ** 2)
                    dx = (verts[-1][0] - v[0]) / dist
            verts[-1]

    def gen_points(self, n, xy_range):
        points = []
        for _ in range(n):
            points.append((random.uniform(*xy_range), random.uniform(*xy_range)))
        return points


SOLUTIONS: List[Base] = [PartA(), PartB(), PartC()]
