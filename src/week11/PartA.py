from Base import Base, AbstractFilenameProvider
import matplotlib.pyplot as plt


def grid_search(x, y):
    assert len(x) == len(y)
    n = len(x)
    a = (n * sum(x_i * y_i for x_i, y_i in zip(x, y)) - sum(x) * sum(y)) / (
        n * sum(x_i ** 2 for x_i in x) - sum(x) ** 2)
    b = sum(y) / n - a * sum(x) / n
    return a, b


def lin_reg(x, y):
    a, b = grid_search(x, y)
    plt.scatter(x, y)
    plt.plot([min(x), max(x)], [a * min(x) + b, a * max(x) + b])
    return plt


def load_data(fn):
    with open(fn) as f:
        return [tuple(map(float, line.split(' '))) for line in f if line]

class PartA(Base):
    name = 'A'

    def run(self, fnprovider: AbstractFilenameProvider):
        plt.clf()
        lin_reg(*zip(*load_data('../resources/w11/linreg.txt'))).savefig(fnprovider.get_filename('.png', 'test', 'test'))
        return fnprovider.format_files()
