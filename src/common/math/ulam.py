from enum import Enum

import numpy as np

from common.python.tuples import add_tuple


class Direction(Enum):
    RIGHT = (0, 1)
    LEFT = (0, -1)
    UP = (-1, 0)
    DOWN = (1, 0)

    def turn_right(self) -> 'Direction':
        return {self.RIGHT: self.UP, self.UP: self.LEFT, self.LEFT: self.DOWN, self.DOWN: self.RIGHT}[self]


def create_ulam(size):
    array = np.zeros((2 * size + 1, 2 * size + 1), dtype=np.uint32)
    array[size][size] = 1
    pos = (size, size + 1)
    direction = Direction.UP
    value = 2
    for i in range(4 * size):
        while array[add_tuple(direction.turn_right().value, pos)] != 0:
            array[pos] = value
            value += 1
            pos = add_tuple(pos, direction.value)
            if pos[0] == array.shape[0] or pos[1] == array.shape[1]:
                break
        direction = direction.turn_right()
    return array
