from typing import Tuple, Callable


def add_tuple(t1: Tuple, t2: Tuple) -> Tuple:
    return tuple(map(lambda x: x[0] + x[1], zip(t1, t2)))


def mult_tuple(t1: Tuple, t2: Tuple) -> Tuple:
    return tuple([a * b for a, b in zip(t1, t2)])


def apply_tuple(fun: Callable[..., Tuple], *tuples: Tuple) -> Tuple:
    return tuple([fun(*row) for row in zip(*tuples)])
