import math

import numpy as np
import svgwrite
import svgwrite.shapes

from Base import Base, AbstractFilenameProvider
from common.datagens.points import *
from common.math.geometry import get_angle, get_direction


def jarvis(points):
    points = list(map(np.array, points))
    left = points[0]
    for p in points:
        if p[0] < left[0]:
            left = p
    hull = [left - (1, 0), left]
    while len(hull) <= 2 or not np.array_equal(hull[1], hull[-1]):
        minangle = (100000, None)
        prev = hull[-2] - hull[-1]
        for v in points:
            if not np.array_equal(v, hull[-1]):
                delta = v - hull[-1]
                angle = 2 * math.pi - get_angle(prev, delta)
                minangle = min(minangle, (angle, v))
        assert minangle[1] is not None
        hull.append(minangle[1])
    return list(map(np.ndarray.tolist, hull))


def graham(points):
    points = list(map(np.array, points))
    leftmost = points[0]
    for p in points:
        if p[0] < leftmost[0]:
            leftmost = p
    left_dir = np.array([-1, 0])
    points_by_angle = []
    for point in points:
        if not np.array_equal(point, leftmost):
            points_by_angle.append((get_angle(left_dir, point - leftmost), point))
    points_by_angle.sort(key=lambda x: x[0])
    hull = [leftmost, points_by_angle[0][1]]
    for _, point in points_by_angle[1:]:
        hull.append(point)
        while len(hull) != 3 and get_direction(hull[-3] - hull[-2], hull[-1] - hull[-2]) == 'R':
            hull[-2] = hull[-1]
            del hull[-1]
    return list(map(np.ndarray.tolist, hull))


class PartC(Base):
    name = 'C'

    def run(self, fnprovider: AbstractFilenameProvider):
        self.eval(fnprovider, gen_points_normal(5000, (50, 200)), 'normal')
        self.eval(fnprovider, gen_points_grid(10, 50, 8, fuzz=3, remove=.2), 'sparse')

        return fnprovider.format_files()

    def eval(self, fnprovider, points, name):
        d = svgwrite.Drawing(fnprovider.get_filename('.svg', f'jarvis_{name}', f'Jarvis on {name}'))
        for point in points:
            d.add(svgwrite.shapes.Circle(center=point, r=2, stroke='blue', fill='lightblue'))
        hull = jarvis(points)
        for idx in range(len(hull)):
            v0, v1 = hull[idx - 1], hull[idx]
            d.add(svgwrite.shapes.Line(v0, v1, stroke='black'))
        d.save()

        d = svgwrite.Drawing(fnprovider.get_filename('.svg', f'graham_{name}', f'Graham on {name}'))
        for point in points:
            d.add(svgwrite.shapes.Circle(center=point, r=2, stroke='blue', fill='lightblue'))
        hull = graham(points)
        for idx in range(len(hull)):
            v0, v1 = hull[idx - 1], hull[idx]
            d.add(svgwrite.shapes.Line(v0, v1, stroke='black'))
        d.save()
