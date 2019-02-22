import numpy as np

from common.python.tuples import add_tuple


def create_ulam(size):
    RIGHT = (0, 1)
    LEFT = (0, -1)
    UP = (-1, 0)
    DOWN = (1, 0)
    right = {RIGHT: UP, UP: LEFT, LEFT: DOWN, DOWN: RIGHT}
    array = np.zeros((2 * size + 1, 2 * size + 1), dtype=np.uint32)
    array[size][size] = 1
    pos = (size, size + 1)
    direction = UP
    value = 2
    for i in range(4 * size):
        while array[add_tuple(right[direction], pos)] != 0:
            array[pos] = value
            value += 1
            pos = add_tuple(pos, direction)
            if pos[0] == array.shape[0] or pos[1] == array.shape[1]:
                break
        direction = right[direction]
    return array