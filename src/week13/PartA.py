import math
import random

import networkx as nx
import svgwrite
import svgwrite.container
import svgwrite.path
import svgwrite.shapes

from Base import Base, AbstractFilenameProvider


def create_circle(n, factor, damping=0) -> nx.Graph:
    g = nx.Graph()
    g.add_node((0, 0))
    prev_cells = 1
    for row in range(1, n):
        cells = _get_cells(row, factor)
        g.add_edge((row, 0), (row, cells - 1), weight=random.random() + damping)
        g.add_edge((row, 0), (row - 1, 0), weight=random.random() + damping)
        for cell in range(1, cells):
            g.add_edge((row, cell - 1), (row, cell), weight=random.random() + damping)
            g.add_edge((row, cell), (row - 1, cell // (cells // prev_cells)), weight=random.random() + damping)
        prev_cells = cells
    return g


def _debug_draw_on_circle(g, n, factor):
    nx.draw_networkx(g, pos=nx.shell_layout(g,
                                            [[(0, 0)]] + [
                                                [(row, col) for col in range(int(math.log2(row + 1)) * factor)] for row
                                                in range(1, n)]))


def _generate_arc(row, cell, cells, layer_depth):
    r = layer_depth * row
    arc = svgwrite.path.Path('m{},0'.format(r))
    arc.push_arc(target=(r * math.cos(2 * math.pi / cells), r * math.sin(2 * math.pi / cells)),
                 rotation=0,
                 r=r,
                 absolute=True,
                 large_arc=False,
                 angle_dir='+')
    arc.rotate(cell * 360 / cells, (0, 0))
    arc.fill(color="none")
    arc.stroke(color="black")
    return arc


def _generate_line(row, cell, cells, layer_depth):
    line = svgwrite.shapes.Line(start=(layer_depth * row, 0), end=(layer_depth * (row + 1), 0), stroke='black')
    line.rotate(cell * 360 / cells, (0, 0))
    return line


def _generate_all_walls(n, factor, layer_depth):
    walls = {}
    prev_cells = 1
    for row in range(1, n):
        cells = _get_cells(row, factor)
        for cell in range(cells):
            walls[(row, cell - 1 if cell != 0 else cells - 1), (row, cell)] = \
                _generate_line(row, cell, cells, layer_depth)
            walls[(row - 1, cell // (cells // prev_cells)), (row, cell)] = _generate_arc(row, cell, cells, layer_depth)
        prev_cells = cells
    return walls


def _get_cells(n, factor):
    return 2**int(math.log2(n + 1)) * factor


def draw_puzzle(factor, tree: nx.Graph, layer_depth: float = 20):
    n = max(r for r, c in tree.nodes) + 1
    svg = svgwrite.Drawing(size=(2 * n * layer_depth, 2 * n * layer_depth))
    walls = _generate_all_walls(n, factor, layer_depth)

    group = svgwrite.container.Group()
    group.translate(n * layer_depth, n * layer_depth)
    svg.add(group)

    for (v1, v2), obj in walls.items():
        if not tree.has_edge(v1, v2):
            group.add(obj)
        else:
            obj.dasharray([3])
            obj.stroke(color="gray")
            group.add(obj)

    cells = _get_cells(n, factor)
    for cell in range(cells):
        group.add(_generate_arc(n, cell, cells, layer_depth))

    return svg


def _get_finish(layer_depth):
    return svgwrite.shapes.Circle(center=(0, 0), r=layer_depth / 3, fill="blue")


def _get_start(tree, factor, layer_depth):
    dists = []
    rows = max(r for r, c in tree.nodes) + 1
    for v in tree.nodes:
        if v[0] == rows-1:
            dists.append((len(nx.shortest_path(tree, v, (0, 0), weight=1)), v))
    dists.sort(reverse=True)
    source = random.choice(dists[:int(len(dists) * 0.2)])[1]
    start = svgwrite.shapes.Circle(center=((source[0] + 0.5) * layer_depth, 0), r=layer_depth / 3, fill="green")
    start.rotate((source[1] + 0.5) * 360 / _get_cells(source[0], factor), center=(0, 0))
    return start


def create_puzzle(n, factor, layer_depth=20, seed=433308):
    random.seed(seed)
    tree = nx.minimum_spanning_tree(create_circle(n, factor))
    puzzle = draw_puzzle(factor, tree, layer_depth=layer_depth)
    group = None
    for element in puzzle.elements:
        if element.elementname == 'g':
            group = element
    group.add(_get_finish(layer_depth))
    group.add(_get_start(tree, factor, layer_depth))
    return puzzle


class PartA(Base):
    name = 'A'

    def run(self, fnprovider: AbstractFilenameProvider):
        with open(fnprovider.get_filename(".svg", "small", "Small (5)"), 'w') as f:
            create_puzzle(5, 2).write(f, pretty=True)

        with open(fnprovider.get_filename(".svg", "medium", "Medium (10)"), 'w') as f:
            create_puzzle(10, 2).write(f, pretty=True)

        with open(fnprovider.get_filename(".svg", "large", "Large (20)"), 'w') as f:
            create_puzzle(20, 2).write(f, pretty=True)

        with open(fnprovider.get_filename(".svg", "large_dense", "Large dense (20)"), 'w') as f:
            create_puzzle(20, 4).write(f, pretty=True)
        return fnprovider.format_files()
