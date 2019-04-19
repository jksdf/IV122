import math
import warnings
from typing import Tuple

from PIL import Image

from Base import Base, AbstractFilenameProvider


def simple_coloring(data):
    if abs(data) <= 2:
        return 0, 0, 0


COLORINGS = {"simple": simple_coloring}


def newton(n: int,
           frame: Tuple[Tuple[float, float], Tuple[float, float]],
           resx: int,
           c: complex,
           coloring):
    assert coloring in COLORINGS.keys()
    xrng, yrng = frame[0][1] - frame[0][0], frame[1][1] - frame[1][0]
    resy = int(resx * yrng / xrng)
    data = [[(xrng * x / resx + frame[0][0]) + (
            yrng * y / resy + frame[1][0]) * 1j
             for x in range(resx)]
            for y in range(resy)]
    for _ in range(n):
        for y in range(resy):
            for x in range(resx):
                old = data[y][x]
                data[y][x] = data[y][x] * data[y][x] + c
                if math.isnan(data[y][x].imag) or math.isnan(data[y][x].real):
                    data[y][x] = old
    img = Image.new("RGB", (resx, resy), color=(255, 255, 255))
    fn = COLORINGS.get(coloring)
    for y in range(resy):
        for x in range(resx):
            try:
                val = fn(data[y][x])
                if val is not None:
                    img.putpixel((x, y), val)
            except Exception as e:
                warnings.warn("issue in mandelbrot")
                raise e
    return img


class PartB(Base):
    name = 'B'

    def run(self, fnprovider: AbstractFilenameProvider):
        newton(20, ((-2, 2), (-1, 1)), 500, -0.73 + 0.19j, 'simple').save(
            fnprovider.get_filename(".png", "newton", "Newton"))
        newton(20, ((-1.2, -0.8), (-0.1, -0.5)), 500, -0.73 + 0.19j, 'simple').save(
            fnprovider.get_filename(".png", "newton_zoomed", "Newton zoomed"))
        return fnprovider.format_files()
