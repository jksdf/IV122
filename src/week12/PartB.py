import itertools
from typing import TextIO, List, Tuple

import networkx as nx

from Base import Base, AbstractFilenameProvider


def load_map(fd: TextIO) -> List[List[str]]:
    return [list(l.strip()) for l in fd if l]


def fac_frac(n, k=None):
    if k is None:
        k = n
    m = 1
    for i in range(n - k + 1, n + 1):
        m *= i
    return m


def get_cell(loc, plane, idx_to_cell, guy_location, crate_locations):
    y, x = loc
    if plane[y][x] == '#':
        return '#'
    if (y, x) == guy_location:
        return 's'
    if (y, x) in (idx_to_cell[i] for i in crate_locations):
        return 'c'
    return ' '


def set_remove_add(tup: Tuple, rem, add):
    assert rem in tup
    x = set(tup)
    x.remove(rem)
    x.add(add)
    return tuple(sorted(x))


def generate_graph(plane: List[List[str]]):
    idx_to_cell = []
    cell_to_idx = {}
    crates = sum(cell == 'c' for row in plane for cell in row)
    for y in range(len(plane)):
        for x in range(len(plane[y])):
            if plane[y][x] != '#':
                cell_to_idx[(y, x)] = len(idx_to_cell)
                idx_to_cell.append((y, x))

    g = nx.DiGraph()
    for guy_location in range(len(idx_to_cell)):
        for crate_locations in itertools.combinations(set(range(len(idx_to_cell))).difference({guy_location}), crates):
            node = (guy_location, tuple(crate_locations))
            g.add_node(node)
            for move in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                new_guy = move[0] + idx_to_cell[guy_location][0], move[1] + idx_to_cell[guy_location][1]
                next_over = get_cell(new_guy, plane, idx_to_cell, guy_location, crate_locations)
                if next_over == ' ':
                    g.add_edge(node, (cell_to_idx[new_guy], tuple(crate_locations)))
                if next_over == 'c':
                    next_crate = move[0] + new_guy[0], move[1] + new_guy[1]
                    two_over = get_cell(next_crate, plane, idx_to_cell, guy_location, crate_locations)
                    if two_over == ' ':
                        crate_idx = cell_to_idx[new_guy]
                        new_crate_idx = cell_to_idx[next_crate]
                        new_node = cell_to_idx[new_guy], set_remove_add(crate_locations, crate_idx, new_crate_idx)
                        assert new_node[0] not in new_node[1]
                        g.add_edge(node, new_node)

    return g, idx_to_cell, cell_to_idx


def get_start_state(plane, cell_to_idx):
    guy_loc = None
    crate_locs = []

    for y in range(len(plane)):
        for x in range(len(plane[y])):
            if plane[y][x] == 's':
                guy_loc = cell_to_idx[(y, x)]
            if plane[y][x] == 'c':
                crate_locs.append(cell_to_idx[(y, x)])
    return guy_loc, tuple(crate_locs)


def get_end_states(plane, cell_to_idx):
    crate_locs = []
    for y in range(len(plane)):
        for x in range(len(plane[y])):
            if plane[y][x] == 'x':
                crate_locs.append(cell_to_idx[(y, x)])

    for guy in set(range(len(cell_to_idx))).difference(crate_locs):
        yield guy, tuple(crate_locs)


def coords_to_moves(coords):
    moves = []
    for a, b in zip(coords[:-1], coords[1:]):
        d = b[0] - a[0], b[1] - a[1]
        if d == (1, 0):
            moves.append('DOWN')
        elif d == (-1, 0):
            moves.append('UP')
        elif d == (0, 1):
            moves.append('RIGHT')
        elif d == (0, -1):
            moves.append('LEFT')
        else:
            raise AssertionError
    return moves


def solve_sokoban(fn):
    with open(fn) as fd:
        plane = load_map(fd)

    empty = sum(cell != '#' for row in plane for cell in row)
    crates = sum(cell == 'c' for row in plane for cell in row)
    states = fac_frac(empty, crates + 1) // fac_frac(crates)

    g, idx_to_cell, cell_to_idx = generate_graph(plane)

    start = get_start_state(plane, cell_to_idx)
    ends = list(get_end_states(plane, cell_to_idx))

    shortest = states,
    for end in ends:
        p = nx.shortest_path(g, start, end)
        shortest = min(shortest, (len(p), p))

    return coords_to_moves([idx_to_cell[x] for x, _ in shortest[1]])


class PartB(Base):
    name = 'B'

    def run(self, fnprovider: AbstractFilenameProvider):
        """Sokoban. Prevzaté z https://www.umimematiku.cz"""
        p1 = solve_sokoban('../resources/w12/sokoban1.txt')
        p2 = solve_sokoban('../resources/w12/sokoban2.txt')
        p3 = solve_sokoban('../resources/w12/sokoban3.txt')
        return fnprovider.format_files(Simple=' -> '.join(p1), Hard=' -> '.join(p2), Slides=' -> '.join(p3))
