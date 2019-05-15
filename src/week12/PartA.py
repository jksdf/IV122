from typing import TextIO, List

import networkx as nx
import numpy as np

from Base import Base, AbstractFilenameProvider


def load_maze(fd: TextIO) -> List[List[int]]:
    n = int(fd.readline())
    res = []
    for _ in range(n):
        res.append(list(map(int, fd.readline().split(' '))))
    return res


def maze_to_graph(maze: List[List[int]]) -> nx.DiGraph:
    g = nx.DiGraph()
    n = len(maze)
    for y in range(n):
        for x in range(n):
            candidates = [maze[y][x] * np.array(i) + (x, y) for i in [(-1, 0), (1, 0), (0, 1), (0, -1)]]
            for c in candidates:
                if np.all(c >= 0) and np.all(c < n):
                    g.add_edge((x, y), tuple(c.tolist()))
    return g


def process(fd):
    maze = load_maze(fd)
    g = maze_to_graph(maze)
    nx.draw_networkx(g, pos={i: i for i in g.nodes})
    paths = nx.all_shortest_paths(g, (0, 0), (len(maze) - 1, len(maze) - 1))
    p0 = next(paths)
    try:
        next(paths)
    except StopIteration:
        return True, p0
    return False, p0


class PartA(Base):
    name = 'A'

    def run(self, fnprovider: AbstractFilenameProvider):
        extra = {}
        with open('../resources/w12/ciselne-bludiste.txt', 'r') as fd:
            i = 0
            while True:
                unique, path = process(fd)
                extra[f'Maze {i}'] = ' -> '.join(map(str, path)) + (' (unique)' if unique else '')
                line = fd.readline()
                if not line.startswith('-'):
                    break
                i += 1
        return fnprovider.format_files(**extra)
