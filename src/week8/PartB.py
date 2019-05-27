from typing import Tuple, Iterable

import numpy as np
import svgwrite
import svgwrite.shapes

from Base import Base, AbstractFilenameProvider
from .PartA import scale, translation, square, write, apply, mult


def mrcm(steps: int, init: Iterable[Tuple[np.ndarray, np.ndarray]], newlocs: Iterable[np.ndarray]) \
        -> Iterable[Tuple[np.ndarray, np.ndarray]]:
    if steps == 0:
        return init
    newlines = []
    prev = mrcm(steps - 1, init, newlocs)
    for loc in newlocs:
        newlines += apply(loc, prev)
    return newlines


def draw_mrcm(steps, init, newlocs,
              viewbox: Tuple[float, float, float, float] = (-20, -20, 140, 140), stroke=1.) -> svgwrite.Drawing:
    img = svgwrite.Drawing(viewBox=','.join(map(str, viewbox)))
    lines = mrcm(steps, init, newlocs)
    write(img, lines, stroke=stroke)
    return img


def square_with_corner(size):
    lines = square(size)
    lines.append((np.array([-size, -size, 1]), np.array([0, 0, 1])))
    return lines


class PartB(Base):
    name = 'B'

    def run(self, fnprovider: AbstractFilenameProvider):
        draw_mrcm(
            5,
            square(25),
            [
                mult(translation(25, 0), scale(0.5, 0.5)),
                mult(translation(0, 50), scale(0.5, 0.5)),
                mult(translation(50, 50), scale(0.5, 0.5))
            ],
            viewbox=(-10, -10, 70, 70),
            stroke=0.5).saveas(fnprovider.get_filename('.svg', 'square_sierpinsky', 'Square Sierpinsky'))

        draw_mrcm(
            5,
            square(25),
            [
                mult(scale(0.5, 0.5)),
                mult(translation(0, 50), scale(0.5, 0.5)),
                mult(translation(50, 50), scale(0.5, 0.5))
            ],
            viewbox=(-10, -10, 70, 70),
            stroke=0.5).saveas(fnprovider.get_filename('.svg', 'square_tilted_sierpinsky', 'Square tilted Sierpinsky'))

        draw_mrcm(
            7,
            apply(translation(25, 25), square(25)),
            [
                mult(translation(0, -50), scale(0.5, -0.5)),
                mult(translation(50, 0), scale(0.5, 0.5)),
                mult(translation(-50, 50), scale(-0.5, 0.5))
            ],
            viewbox=(-10, -10, 70, 70),
            stroke=0.1).saveas(fnprovider.get_filename('.svg', 'sierpinsky_var1', 'Sierpinsky variant 1'))

        draw_mrcm(
            1,
            apply(translation(25, 25), square_with_corner(25)),
            [
                mult(translation(0, -50), scale(0.5, -0.5)),
                mult(translation(50, 0), scale(0.5, 0.5)),
                mult(translation(-50, 50), scale(-0.5, 0.5))
            ],
            viewbox=(-10, -10, 70, 70),
            stroke=0.1).saveas(
            fnprovider.get_filename('.svg', 'sierpinsky_var1_1step', 'Sierpinsky variant 1 (1 step)'))

        return fnprovider.format_files()
