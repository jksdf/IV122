import numpy as np
import svgwrite
import svgwrite.drawing
import svgwrite.shapes
from PIL import Image

from Base import Base
from common.python.tuples import add_tuple, mult_tuple


def corner(drawing: svgwrite.drawing.Drawing, size: int = 100, steps=10, pos=(0, 0), direction=(1, 1)):
    def transform(x):
        return add_tuple(pos, mult_tuple(direction, x))

    for i in range(steps + 1):
        p = size / steps * i
        drawing.add(svgwrite.shapes.Line(transform((p, 0)), transform((size, p)), stroke='black'))


def star(drawing: svgwrite.drawing.Drawing, steps=10, pos=(0, 0)):
    corner(drawing, pos=add_tuple(pos, (0, 100)), direction=(1, 1), steps=steps)
    corner(drawing, pos=add_tuple(pos, (200, 100)), direction=(-1, 1), steps=steps)
    corner(drawing, pos=add_tuple(pos, (0, 100)), direction=(1, -1), steps=steps)
    corner(drawing, pos=add_tuple(pos, (200, 100)), direction=(-1, -1), steps=steps)


def inverse_star(drawing: svgwrite.drawing.Drawing, steps=10, pos=(0, 0)):
    corner(drawing, pos=add_tuple(pos, (100, 0)), direction=(1, 1), steps=steps)
    corner(drawing, pos=add_tuple(pos, (100, 0)), direction=(-1, 1), steps=steps)
    corner(drawing, pos=add_tuple(pos, (100, 200)), direction=(1, -1), steps=steps)
    corner(drawing, pos=add_tuple(pos, (100, 200)), direction=(-1, -1), steps=steps)


def small_inverse_square(drawing: svgwrite.drawing.Drawing, steps=10, pos=(0, 0)):
    corner(drawing, pos=add_tuple(pos, (0, 0)), direction=(1, 1), steps=steps)
    corner(drawing, pos=add_tuple(pos, (100, 0)), direction=(-1, 1), steps=steps)
    corner(drawing, pos=add_tuple(pos, (100, 100)), direction=(-1, -1), steps=steps)
    corner(drawing, pos=add_tuple(pos, (0, 100)), direction=(1, -1), steps=steps)


class PartB(Base):
    name = 'B'

    def run(self, fnprovider):
        imgdim = 300
        imgsize = (imgdim, imgdim)
        image_array = np.dstack((np.fromfunction(lambda x, y: 256 * y / imgdim, shape=imgsize, dtype=np.uint32),
                                 np.zeros(shape=imgsize, dtype=np.uint32),
                                 np.fromfunction(lambda x, y: 256 * x / imgdim, shape=imgsize, dtype=np.uint32)))
        image = Image.fromarray(np.uint8(image_array))
        image.save(fnprovider.get_filename('.png', 'raster', 'Raster'))

        drawing = svgwrite.Drawing(fnprovider.get_filename('.svg', 'star', 'Star'), size=(400, 400))
        star(drawing, pos=(0, 0))
        star(drawing, pos=(200, 0), steps=30)
        inverse_star(drawing, pos=(0, 200))
        small_inverse_square(drawing, pos=(250, 250))
        drawing.save()
        return fnprovider.format_files()
