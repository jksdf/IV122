import random

import matplotlib.pyplot as plt

from Base import Base, AbstractFilenameProvider


def analytical_solution(x, y):
    assert len(x) == len(y)
    n = len(x)
    a = (n * sum(x_i * y_i for x_i, y_i in zip(x, y)) - sum(x) * sum(y)) / (
            n * sum(x_i ** 2 for x_i in x) - sum(x) ** 2)
    b = sum(y) / n - a * sum(x) / n
    return a, b


def gradient_descent(x, y, iters, init=None, lr=0.1):
    if init is None:
        a, b = random.uniform(0, 1), random.uniform(min(x), max(x))
    else:
        a, b = init
    for _ in range(iters):
        grad_a = 2/len(x) * (-sum(xi * (yi - (a * xi + b)) for xi, yi in zip(x, y)))
        grad_b = 2/len(x) * (-sum(yi - (a * xi + b) for xi, yi in zip(x, y)))
        a -= lr * grad_a
        b -= lr * grad_b
    return a, b


def lin_reg(x, y):
    plt.clf()
    analytical_a, analytical_b = analytical_solution(x, y)
    grad_desc_a, grad_desc_b = gradient_descent(x, y, 50)
    plt.scatter(x, y)
    plt.plot([min(x), max(x)], [analytical_a * min(x) + analytical_b, analytical_a * max(x) + analytical_b], color="blue")
    plt.plot([min(x), max(x)], [grad_desc_a * min(x) + grad_desc_b, grad_desc_a * max(x) + grad_desc_b], color="yellow")
    return plt


def load_data(fn):
    with open(fn) as f:
        return [tuple(map(float, line.split(' '))) for line in f if line]


def generate_with_dist(n: int, error_dist, dist):
    """
    Generates points along a random line with distribution dist and error error_dist.
    :param n: number of points
    :param error_dist: distribution of noise (should return with average in 0)
    :param dist: distribution along the line (should return in [0;1) range)
    :return: list of x,y coordinates tuples
    """
    a = random.random() * 4 - 2
    b = random.random()
    points = []
    for i in range(n):
        x = -1
        while x > 1 or x < 0:
            x = dist()
        y_real = a * x + b
        y_noisy = y_real + error_dist()
        points.append((x, y_noisy))
    return a, b, points


def visualize_generated(error_dist, dist, n=100, seed=433308):
    random.seed(seed)
    a, b, points = generate_with_dist(n, error_dist, dist)
    x, y = zip(*points)
    lin_reg(x, y)
    plt.plot([0, 1], [b, a + b], color="red")
    plt.legend(["Calculated", "Grad. desc.", "Actual"])
    return plt


class PartA(Base):
    name = 'A'

    def run(self, fnprovider: AbstractFilenameProvider):
        plt.clf()
        lin_reg(*zip(*load_data('../resources/w11/linreg.txt'))).savefig(
            fnprovider.get_filename('.png', 'linreg', 'Linreg'))

        visualize_generated(lambda: random.uniform(-1, 1), random.random) \
            .savefig(fnprovider.get_filename('.png', 'even_dist', 'Even distribution'))
        visualize_generated(lambda: random.gauss(0, 1), random.random) \
            .savefig(fnprovider.get_filename('.png', 'gauss_dist', 'Gaussian distribution'))

        visualize_generated(lambda: random.gauss(0, 1), lambda: random.lognormvariate(0, 1)) \
            .savefig(fnprovider.get_filename('.png', 'gauss_log-normal_dist',
                                             'Gaussian distribution with log-normal along the line'))
        return fnprovider.format_files()
