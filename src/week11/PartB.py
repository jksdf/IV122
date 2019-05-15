import random
from typing import List, Optional

import numpy as np
import svgwrite, svgwrite.shapes

from Base import Base, AbstractFilenameProvider


def closest(point: np.ndarray, options):
    s = sum((point - options[0]) ** 2), 0
    for idx, option in enumerate(options[1:]):
        s = min(s, (sum((point - option) ** 2), idx))
    return s[1]


def kmeans(points: List[np.ndarray], init: Optional[List[np.ndarray]] = None,
           n: Optional[int] = None, iterations: int = 10):
    assert not (init is not None and n is not None)
    if init is None:
        init = random.sample(points, n)

    selected = init

    for _ in range(iterations):
        clusters = [[] for _ in selected]
        for point in points:
            clusters[closest(point, selected)].append(point)
        selected = [sum(cluster) / len(cluster) if len(cluster) != 0 else selected[idx] for idx, cluster in enumerate(clusters)]
    return selected


class PartB(Base):
    name = 'B'

    def run(self, fnprovider: AbstractFilenameProvider):
        d = svgwrite.Drawing(fnprovider.get_filename(".svg", "test", "test"), size=(700,700))
        points = []
        for _ in range(20):
            points.append(np.array([random.random(), random.random()]))
        for _ in range(20):
            points.append(np.array([5+random.random(), 5+random.random()]))
        for point in points:
            d.add(svgwrite.shapes.Circle((point*100).tolist(), r=1))
        centers = kmeans(points, n=2)
        for center in centers:
            d.add(svgwrite.shapes.Circle((center*100).tolist(), r=10, color='red'))
        d.save()
        return fnprovider.format_files()
