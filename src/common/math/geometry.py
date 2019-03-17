import math

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