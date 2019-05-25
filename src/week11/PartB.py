import math
import random
from typing import List, Optional, Tuple

import matplotlib
import matplotlib.colors
import numpy as np
import svgwrite
import svgwrite.animate
import svgwrite.shapes
import svgwrite.text

from Base import Base, AbstractFilenameProvider
from common.math.geometry import rotate


def closest(point: np.ndarray, options):
    dists = [(sum((point - option) ** 2), idx) for idx, option in enumerate(options)]
    return min(dists)[1]


def kmeans(points: List[np.ndarray], init_idxs: Optional[List[int]] = None,
           n: Optional[int] = None, iterations: int = 10):
    assert init_idxs is None or n == len(init_idxs)
    random.seed(433308)
    if init_idxs is None:
        init = random.sample(points, n)
    else:
        init = [points[i] for i in init_idxs]

    selected = init
    clusters = [[] for _ in selected]

    for _ in range(iterations):
        clusters = [[] for _ in selected]
        for point in points:
            clusters[closest(point, selected)].append(point)
        selected = [sum(cluster) / len(cluster) if len(cluster) != 0 else selected[idx] for idx, cluster in
                    enumerate(clusters)]
    return clusters, selected


def generate_square(n: int, pos: Tuple[float, float], size: Tuple[float, float]) -> List[np.ndarray]:
    pos = np.array(pos)
    size = np.array(size)
    return [pos + np.array([random.random(), random.random()] * size) for _ in range(n)]


def generate_circle_gauss(n: int, pos: Tuple[float, float], sigma: float) -> List[np.ndarray]:
    pos = np.array(pos)
    return [pos + rotate(np.array([0, random.gauss(0, sigma)]), random.uniform(0, math.pi)) for _ in range(n)]


def animate(steps, n, points, colors, size, x_scale=1, scale=1, init_idxs=None):
    size *= scale
    d = svgwrite.Drawing(size=(size, size))
    for i in range(steps):
        t = svgwrite.text.Text(f'{i}')
        t.attribs['x'] = "0"
        t.attribs['y'] = str(size - 30)
        t.attribs['font-size'] = '50'
        t.attribs['display'] = "none"
        t.add(svgwrite.animate.Animate(attributeName='display',
                                       values='none;inline;none;none',
                                       keyTimes=f'0;{i / steps};{(i + 1) / steps};1',
                                       repeatCount="indefinite",
                                       dur=f"{steps}s",
                                       begin="0s"))
        d.add(t)

    pcols = {Hashable(p): [] for p in points}
    for t in range(1, steps + 1):
        clusters, centers = kmeans(points, n=n, iterations=t, init_idxs=init_idxs)
        for cluster, color in zip(clusters, colors[:-1]):
            for point in cluster:
                pcols[Hashable(point)].append(color)

    sequence = [0]
    for i in range(1, steps):
        sequence.append(i / steps)
        sequence.append(i / steps)
    sequence.append(1)
    sequence = ';'.join(map(str, sequence))

    for point, colors in pcols.items():
        cs = []
        for c in colors:
            cs.append(c)
            cs.append(c)
        point = point.array
        x, y = (point * scale).tolist()
        x *= x_scale
        c = svgwrite.shapes.Circle((x, y), r=3, fill="black")
        c.add(svgwrite.animate.Animate(attributeType="XML",
                                       attributeName="fill",
                                       values=';'.join(cs),
                                       dur=f"{steps}s",
                                       begin="0s",
                                       keyTimes=sequence,
                                       repeatCount="indefinite"))
        d.add(c)
    return d


class Hashable:
    def __init__(self, array: np.ndarray):
        self.array = array

    def __hash__(self):
        return tuple(map(int, self.array.tolist())).__hash__()

    def __eq__(self, other):
        return type(other) == Hashable and other.array is self.array


def load_points(fn):
    with open(fn, 'r') as fd:
        return [np.array(list(map(float, i.split()))) for i in fd if i]


class PartB(Base):
    name = 'B'

    def run(self, fnprovider: AbstractFilenameProvider):
        random.seed(433308)

        colors = list(matplotlib.colors.TABLEAU_COLORS.values())
        animate(5,
                3,
                sum([generate_circle_gauss(50, (200, 200), 20),
                     generate_circle_gauss(80, (300, 200), 30),
                     generate_circle_gauss(50, (380, 350), 50)],
                    []),
                colors,
                500).saveas(fnprovider.get_filename(".svg", "example1", "Distinct clusters"), pretty=True)

        animate(5,
                3,
                sum([generate_circle_gauss(100, (200, 200), 50),
                     generate_circle_gauss(100, (300, 200), 50),
                     generate_circle_gauss(50, (380, 350), 50)],
                    []),
                colors,
                500).saveas(fnprovider.get_filename(".svg", "example2", "2 merged clusters"), pretty=True)

        animate(13,
                3,
                sum([generate_circle_gauss(200, (200, 200), 50),
                     generate_circle_gauss(200, (250, 200), 50),
                     generate_circle_gauss(50, (380, 350), 50)],
                    []),
                colors,
                500,
                init_idxs=[0,1,2]).saveas(fnprovider.get_filename(".svg", "example3", "2 merged clusters (very close)"), pretty=True)

        animate(6, 2, load_points('../resources/w11/faithful.txt'), colors, 150, x_scale=10, scale=5,
                init_idxs=[54, 222]).saveas(
            fnprovider.get_filename(".svg", "faithful", "Faithful"), pretty=True)

        return fnprovider.format_files()
