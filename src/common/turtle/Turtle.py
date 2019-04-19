import math
from enum import Enum
from typing import Optional

import svgwrite
import svgwrite.shapes

from common.math.geometry import deg2rad
from common.python.tuples import add_tuple


class PenStates(Enum):
    UP = 0
    DOWN = 1


class Turtle:
    def __init__(self, fn, basepos=(0,0)):
        self.drawing = svgwrite.Drawing(fn)
        self.pen = PenStates.DOWN
        self.position = 0
        self.angle = 0
        self.basepos = basepos
        self.resetpos()

    def forward(self, dist, usepen: Optional[bool] = None, color='black', thickness=None):
        radang = deg2rad(self.angle)
        nextpos = add_tuple(self.position, (math.cos(radang) * dist, math.sin(radang) * dist))
        if (usepen is None and self.pen == PenStates.DOWN) or (usepen is not None and usepen):
            self.line(self.position, nextpos, color, thickness)
        self.position = nextpos

    def right(self, angle):
        self.angle = (self.angle + angle) % 360

    def left(self, angle):
        self.right(-angle)

    def back(self, dist, usepen: Optional[bool] = None):
        self.forward(-dist, usepen)

    def pendown(self):
        self.pen = PenStates.DOWN

    def penup(self):
        self.pen = PenStates.UP

    def line(self, start, end, color='black', thickness=None):
        self.drawing.add(svgwrite.shapes.Line(start=start, end=end, stroke=color, stroke_width=thickness if thickness else 1))

    def resetpos(self, position=(0, 0), angle=0):
        self.position = position[0] + self.basepos[0], position[1] + self.basepos[1]
        self.angle = angle

    def save(self, fn=None, frame=None):
        if frame is not None:
            self.drawing['width'], self.drawing['height'] = add_tuple(frame, self.basepos)
        if fn:
            self.drawing.saveas(fn)
        else:
            self.drawing.save()

    def __str__(self):
        return f'[{self.position}@{self.angle}]'
