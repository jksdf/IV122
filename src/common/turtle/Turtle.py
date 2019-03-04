from enum import Enum

import math
import svgwrite

import svgwrite.shapes

from src.common.python.tuples import add_tuple


class PenStates(Enum):
    UP = 0
    DOWN = 1


class Turtle:
    def __init__(self, fn):
        self.drawing = svgwrite.Drawing(fn)
        self.pen = PenStates.DOWN
        self.position = (500, 500)
        self.angle = 0
        self.min = (0, 0)

    def forward(self, dist):
        radang = deg2rad(self.angle)
        nextpos = add_tuple(self.position, (math.cos(radang) * dist, math.sin(radang) * dist))
        if self.pen == PenStates.DOWN:
            self.min = tuple(map(min, zip(self.min, nextpos)))
            self.drawing.add(svgwrite.shapes.Line(start=self.position, end=nextpos, stroke='black'))
        self.position = nextpos

    def right(self, angle):
        self.angle = (self.angle + angle) % 360

    def left(self, angle):
        self.right(-angle)

    def back(self, dist):
        self.forward(-dist)

    def pendown(self):
        self.pen = PenStates.DOWN

    def penup(self):
        self.pen = PenStates.UP

    def save(self, fn=None):
        if fn:
            self.drawing.saveas(fn)
        else:
            self.drawing.save()


def deg2rad(deg):
    return deg / 180 * math.pi
