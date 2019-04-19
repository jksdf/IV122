from math import sin, cos
from typing import List, Iterable, Tuple

import numpy as np
import svgwrite
import svgwrite.shapes

from Base import Base, AbstractFilenameProvider


def rotation(theta: float) -> np.ndarray:
    theta = np.deg2rad(theta)
    return np.array([[cos(theta), -sin(theta), 0],
                     [sin(theta), cos(theta), 0],
                     [0, 0, 1]])


def translation(dx: float, dy: float) -> np.ndarray:
    return np.array([[1, 0, dx],
                     [0, 1, dy],
                     [0, 0, 1]])


def shear(k: float) -> np.ndarray:
    return np.array([[1, k, 0],
                     [0, 1, 0],
                     [0, 0, 1]])


def mat(a=0., b=0., c=0., d=0., e=0., f=0.) -> np.ndarray:
    return np.array([[a, c, e],
                     [b, d, f],
                     [0, 0, 1]])


def scale(a: float, b: float) -> np.ndarray:
    return np.array([[a, 0, 0],
                     [0, b, 0],
                     [0, 0, 1]])


def square(size: float) -> List[Tuple[np.ndarray, np.ndarray]]:
    points = [np.transpose(np.array(p)) for p in
              [(-size, -size, 1), (-size, size, 1), (size, size, 1), (size, -size, 1)]]
    return [(points[idx], points[idx + 1]) for idx in range(-1, len(points) - 1)]


def line(size: float) -> List[Tuple[np.ndarray, np.ndarray]]:
    return [(np.transpose(np.array((0, 0, 1))), np.transpose(np.array((size, 0, 1))))]


def vec2tup(vec: np.ndarray) -> Tuple[float, float]:
    return tuple(np.transpose(vec).tolist()[:2])


def write(img: svgwrite.Drawing, lines: Iterable[Tuple[np.ndarray, np.ndarray]]) -> None:
    for a, b in lines:
        img.add(svgwrite.shapes.Line(vec2tup(a), vec2tup(b), stroke='black', stroke_width='0.1'))


def apply(mat: np.ndarray, lines: Iterable[Tuple[np.ndarray, np.ndarray]]) -> List[Tuple[np.ndarray, np.ndarray]]:
    return [(np.dot(mat, a), np.dot(mat, b)) for a, b in lines]


ONE = scale(1, 1)


def mult(*mats: np.ndarray) -> np.ndarray:
    val = ONE
    for mat in mats:
        val = np.dot(val, mat)
    return val


def demo(fn: str, viewbox: Tuple[float, float, float, float], stepcount: int,
         steps: Iterable[np.ndarray], init=None) -> svgwrite.Drawing:
    if init is None:
        init = square(100)
    img = svgwrite.Drawing(fn, viewBox=','.join(map(str, viewbox)))
    mat = ONE
    step = mult(*steps)
    for _ in range(stepcount):
        write(img, apply(mat, init))
        mat = mult(mat, step)
    return img


def example1(fn: str) -> svgwrite.Drawing:
    return demo(fn, (-400, -150, 600, 1000), 10, (rotation(10), scale(1.1, 1.1), translation(20, 40)))


def example2(fn: str) -> svgwrite.Drawing:
    return demo(fn, (-200, -200, 400, 400), 15, (rotation(10), scale(1.1, 0.8)))


def example3(fn: str) -> svgwrite.Drawing:
    return demo(fn, (-200, -150, 350, 450), 25,
                (rotation(20), scale(0.9, 0.9), translation(40, 40)))


class PartA(Base):
    name = 'A'

    def run(self, fnprovider: AbstractFilenameProvider):
        example1(fnprovider.get_filename('.svg', 'example1', 'Example1')).save()
        example2(fnprovider.get_filename('.svg', 'example2', 'Example2')).save()
        example3(fnprovider.get_filename('.svg', 'example3', 'Example3')).save()
        return fnprovider.format_files()
