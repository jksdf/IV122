from typing import List

import math

from common.geometry.geometry import deg2rad
from src.common.turtle.Turtle import Turtle
from src.Base import Base, AbstractFilenameProvider


def polygon(turtle: Turtle, n: int, size: float):
    angle = 360 / n
    for _ in range(n):
        turtle.forward(size)
        turtle.right(angle)


def star(turtle: Turtle, n: int, size: float):
    angle = 180 - 2 * (90 - 360 / n)
    for _ in range(n):
        turtle.forward(size)
        turtle.right(angle)


class PartA(Base):
    name = 'A'

    def run(self, fnprovider: AbstractFilenameProvider):
        fn = fnprovider.get_filename(suffix='.svg', name="polygon")
        turtle = Turtle(fn)
        polygon(turtle, 5, 50)
        turtle.penup()
        turtle.forward(100)
        turtle.pendown()
        star(turtle, 5, 50)
        turtle.penup()
        turtle.forward(100)
        turtle.pendown()
        star(turtle, 7, 50)
        turtle.save()
        return fn


class PartB(Base):
    name = 'B'

    def run(self, fnprovider: AbstractFilenameProvider):
        angle = 180 - 360 / 5
        fn = fnprovider.get_filename(suffix='.svg', name="polygon")
        turtle = Turtle(fn)
        star(turtle, 5, math.sqrt(2 * 100 * 100 - 2 * 100 * 100 * math.cos(deg2rad(angle))))
        turtle.left((180 - angle) / 2)
        polygon(turtle, 5, 100)
        turtle.save()
        return fn


SOLUTIONS: List[Base] = [PartA(), PartB()]
