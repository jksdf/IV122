import random
from numbers import Real
from typing import List, Tuple, Any, Sequence, Optional

import networkx as nx
import numpy as np
import svgwrite
import svgwrite.shapes

from Base import Base, AbstractFilenameProvider
from common.datagens.points import gen_points_normal, gen_points_grid
from common.math.geometry import line_len, intersect_linesegments, get_angle


def greedy(points) -> List:
    triangulation: List[Tuple[Tuple, Tuple]] = []
    lines = []
    for idx1 in range(len(points)):
        for idx2 in range(idx1 + 1, len(points)):
            v1, v2 = points[idx1], points[idx2]
            lines.append((line_len(v1, v2), (v1, v2)))
    lines.sort(key=lambda x: x[0])
    for _, line in lines:
        does_intersect = False
        for existing in triangulation:
            intersection = intersect_linesegments(line, existing)
            if intersection is not None \
                    and not np.allclose(intersection, line[0]) \
                    and not np.allclose(intersection, line[1]):
                does_intersect = True
                break
        if not does_intersect:
            triangulation.append(line)
    return triangulation


def delaunay(points: Sequence[Tuple[Real, Real]], init_triangulation=greedy) -> List:
    """Super slow implementation of Delaunay triangulation."""
    triangulation = init_triangulation(points)
    graph = nx.Graph()
    graph.add_nodes_from(points)
    for a, b in triangulation:
        graph.add_edge(a, b)
    for a in graph.nodes:
        verts = _find_conflict(graph, a)
        while verts is not None:
            b, c, d = verts
            graph.remove_edge(b, c)
            graph.add_edge(a, d)
            verts = _find_conflict(graph, a)
    return list(graph.edges)


def _find_conflict(graph, a) -> Optional[Tuple[Any, Any, Any]]:
    neighbours = [(get_angle((1, 0), n), n) for n in graph[a]]
    neighbours.sort(key=lambda x: x[0])
    neighbours = [n[1] for n in neighbours]
    for bidx in range(len(neighbours)):
        b = neighbours[bidx]
        c = neighbours[bidx - 1]
        if graph.has_edge(b, c):
            for d in set(graph[b]).intersection(set(graph[c])):
                if d not in (a, b, c):
                    triangle_area = np.linalg.det([[1, 1, 1], [a[0], b[0], c[0]], [a[1], b[1], c[1]]]) / 2
                    if triangle_area > 0:
                        b, c = c, b
                    det = np.linalg.det([[x[0], x[1], x[0] ** 2 + x[1] ** 2, 1] for x in (a, b, c, d)])
                    if det < 0:
                        return b, c, d
    return None


class PartB(Base):
    name = 'B'

    def run(self, fnprovider: AbstractFilenameProvider):
        random.seed(433308)
        self.eval(fnprovider, gen_points_normal(50, (5, 405)), 'normal')

        random.seed(433308 * 2)
        self.eval(fnprovider, gen_points_grid(10, 5, 40, fuzz=5), 'grid')

        random.seed(433308 * 2)
        self.eval(fnprovider, gen_points_grid(10, 5, 40, fuzz=5, remove=0.2), 'sparse')

        return fnprovider.format_files()

    def eval(self, fnprovider, points, name):
        lines = greedy(points)
        d = svgwrite.Drawing(fnprovider.get_filename('.svg', f'greedy_{name}', f'Greedy on {name}'), size=(415, 415))
        for start, end in lines:
            d.add(svgwrite.shapes.Line(start, end, stroke='black'))
        for point in points:
            d.add(svgwrite.shapes.Circle(center=point, r=2, stroke='blue', fill='lightblue'))
        d.save()
        lines = delaunay(points)
        d = svgwrite.Drawing(fnprovider.get_filename('.svg', f'delaunay_{name}', f'Delaunay on {name}'), size=(415, 415))
        for start, end in lines:
            d.add(svgwrite.shapes.Line(start, end, stroke='black'))
        for point in points:
            d.add(svgwrite.shapes.Circle(center=point, r=2, stroke='blue', fill='lightblue'))
        d.save()
