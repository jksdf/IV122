from typing import Tuple, Iterable

import numpy as np
import svgwrite

from Base import Base, AbstractFilenameProvider
from .PartA import scale, translation, square, write, apply, mult, mat, line


def mrcm(steps: int, init: Iterable[Tuple[np.ndarray, np.ndarray]], newlocs: Iterable[np.ndarray]) \
        -> Iterable[Tuple[np.ndarray, np.ndarray]]:
    if steps == 0:
        return init
    newlines = []
    prev = mrcm(steps - 1, init, newlocs)
    for loc in newlocs:
        newlines += apply(loc, prev)
    return newlines


def draw_mrcm(fn, steps, init, newlocs,
              viewbox: Tuple[float, float, float, float] = (-20, -20, 140, 140)) -> svgwrite.Drawing:
    img = svgwrite.Drawing(fn, viewBox=','.join(map(str, viewbox)))
    lines = mrcm(steps, init, newlocs)
    write(img, lines)
    return img


class PartB(Base):
    name = 'B'

    def run(self, fnprovider: AbstractFilenameProvider):
        draw_mrcm(fnprovider.get_filename('.svg', 'square_sierpinsky', 'Square Sierpinsky'), 5, square(100),
                  [mult(translation(25, 0), scale(0.5, 0.5)),
                   mult(translation(0, 50), scale(0.5, 0.5)),
                   mult(translation(50, 50), scale(0.5, 0.5))]).save()

        draw_mrcm(fnprovider.get_filename('.svg', 'square_tilted_sierpinsky', 'Square tilted Sierpinsky'), 5,
                  square(100),
                  [mult(scale(0.5, 0.5)),
                   mult(translation(0, 50), scale(0.5, 0.5)),
                   mult(translation(50, 50), scale(0.5, 0.5))]).save()

        draw_mrcm(fnprovider.get_filename('.svg', 'sierpinsky_var1', 'Sierpinsky variant 1'), 5,
                  square(100),
                  [mult(translation(50, 0), scale(-0.5, 0.5)),
                   mult(translation(0, 50), scale(0.5, 0.5)),
                   mult(translation(50, 100), scale(0.5, -0.5))]).save()

        # TODO: does not work
        draw_mrcm(fnprovider.get_filename('.svg', 'barnsley_fern0', 'Barnsley fern0'), 0,
                  apply(mult(translation(0, -1), scale(1, 2)), square(1)),
                  [mat(0.849, 0.037, -0.037, 0.849, 0.075, 0.183),
                   mat(0.197, -0.226, 0.226, 0.197, 0.4, 0.049),
                   mat(-0.15, 0.283, 0.26, 0.237, 0.575, 0.084),
                   mat(d=0.16, e=0.5)], viewbox=(-10,-10,20,20)).save()
        draw_mrcm(fnprovider.get_filename('.svg', 'barnsley_fern1', 'Barnsley fern1'), 2,
                  apply(mult(translation(0, -1), scale(1, 2)), square(1)),
                  [mat(0.849, 0.037, -0.037, 0.849, 0.075, 0.183),
                   mat(0.197, -0.226, 0.226, 0.197, 0.4, 0.049),
                   mat(-0.15, 0.283, 0.26, 0.237, 0.575, 0.084),
                   mat(d=0.16, e=0.5)], viewbox=(-10,-10,20,20)).save()

        draw_mrcm(fnprovider.get_filename('.svg', 'star', 'Star'), 1,
                  line(100),
                  [mat(0.255, 0, 0, 0.255, 0.3726, 0.6714),
                   mat(0.255, 0, 0, 0.255, 0.1146, 0.2232),
                   mat(0.255, 0, 0, 0.255, 0.6306, 0.2232),
                   mat(0.370, -0.642, 0.642, 0.370, 0.6356, -0.0061)]).save()

        return fnprovider.format_files()
