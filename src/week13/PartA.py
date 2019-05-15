import math
import random

from Base import Base, AbstractFilenameProvider
import networkx as nx
import matplotlib.pyplot as plt


def create_circle(n, damping=0) -> nx.Graph:
    g = nx.Graph()
    g.add_node((0, 0))
    prev_cells = 1
    for row in range(1, n):
        cells = int(math.log2(row + 1)) * 4
        g.add_edge((row, 0), (row, cells - 1), weight=random.random() + damping)
        g.add_edge((row, 0), (row - 1, 0), weight=random.random() + damping)
        for cell in range(1, cells):
            g.add_edge((row, cell - 1), (row, cell), weight=random.random() + damping)
            g.add_edge((row, cell), (row - 1, cell // (cells // prev_cells)), weight=random.random() + damping)
        prev_cells = cells
    return g

def draw_on_circle(g, n):
    nx.draw_networkx(g, pos=nx.shell_layout(g,
                                            [[(0, 0)]] + [[(row, col) for col in range(int(math.log2(row + 1)) * 4)] for
                                                          row in range(1, n)]))

class PartA(Base):
    name = 'A'

    def run(self, fnprovider: AbstractFilenameProvider):
        random.seed(433308)
        g = create_circle(5)
        draw_on_circle(g, 5)
        print(g.edges)
        plt.savefig(fnprovider.get_filename(".png", "circle", "circle"))
        tree = nx.minimum_spanning_tree(g)
        plt.clf()
        draw_on_circle(g, 5)
        plt.savefig(fnprovider.get_filename(".png", "tree", "tree"))
        return fnprovider.format_files()
