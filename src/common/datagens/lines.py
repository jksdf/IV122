import math
import random
from numbers import Real
from typing import Tuple


def gen_line_segments(n, length, xy_range: Tuple[Real, Real]):
    lines = []
    for _ in range(n):
        x, y = random.uniform(*xy_range), random.uniform(*xy_range)
        angle = random.uniform(0, 2 * math.pi)
        lines.append(((x, y), (x + math.cos(angle) * length, y + math.sin(angle) * length)))
    return lines