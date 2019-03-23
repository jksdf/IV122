import math
from numbers import Real
from typing import Optional, Tuple

import numpy as np


def deg2rad(deg):
    return deg / 180 * math.pi


def rad2deg(rad):
    return rad / math.pi * 180


def normalize(v: np.array) -> np.array:
    norm = np.linalg.norm(v, ord=1)
    if norm == 0:
        norm = np.finfo(v.dtype).eps
    return v / norm


def get_angle(v1, v2) -> Real:
    if (v1[0] == 0 and v1[1] == 0) or (v2[0] == 0 and v2[1] == 0):
        return 2 * math.pi
    dot = v1[0] * v2[0] + v1[1] * v2[1]  # dot product
    det = v1[0] * v2[1] - v1[1] * v2[0]  # determinant
    angle = math.atan2(det, dot)  # atan2(y, x) or atan2(sin, cos)
    if angle < 0:
        return 2 * math.pi + angle
    return angle


def get_direction(v1: np.ndarray, v2: np.ndarray) -> str:
    """Returns 'R' if v2 in to the right of v1, 'L' if to the left. 'C' if colinear."""
    assert len(v1) == 2 and len(v2) == 2
    val = v1[0] * v2[1] - v1[1] * v2[0]
    if val > 0:
        return 'R'
    elif val == 0:
        return 'C'
    elif val < 0:
        return 'L'


def line_len(v1, v2):
    if type(v1) is not np.ndarray:
        v1 = np.array(v1)
    if type(v2) is not np.ndarray:
        v2 = np.array(v2)
    return math.sqrt(np.sum((v1 - v2) ** 2))


def intersect_linesegments(segment1, segment2) -> Optional[Tuple[Real, Real]]:
    (x1, y1), (x2, y2) = segment1
    (x3, y3), (x4, y4) = segment2
    xden = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
    yden = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
    if xden == 0 or yden == 0:  # colinear
        if x1 < x3 < x2:
            return x3
        if x1 < x4 < x2:
            return x4
        if y1 < y3 < y2:
            return y3
        if y1 < y4 < y2:
            return y4
        return None
    x = ((x1 * y2 - y1 * x2) * (x3 - x4) - (x1 - x2) * (x3 * y4 - y3 * x4)) / xden
    y = ((x1 * y2 - y1 * x2) * (y3 - y4) - (y1 - y2) * (x3 * y4 - y3 * x4)) / yden
    if min(x1, x2) <= x <= max(x1, x2) and min(x3, x4) <= x <= max(x3, x4) \
            and min(y1, y2) <= y <= max(y1, y2) and min(y3, y4) <= y <= max(y3, y4):
        return x, y
    return None
