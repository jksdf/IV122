from typing import List

from src.common.turtle.Turtle import Turtle
from src.Base import Base, AbstractFilenameProvider


class PartA(Base):
    name = 'A'

    def run(self, fnprovider: AbstractFilenameProvider):
        fn = fnprovider.get_filename(suffix='.svg', name="polygon")
        turtle = Turtle(fn)
        self.polygon(turtle, 5, 50)
        turtle.penup()
        turtle.forward(100)
        turtle.pendown()
        self.star(turtle, 5, 50)
        turtle.penup()
        turtle.forward(100)
        turtle.pendown()
        self.star(turtle, 7, 50)
        turtle.save()
        return fn

    def polygon(self, turtle: Turtle, n: int, size: float):
        angle = 360 / n
        for _ in range(n):
            turtle.forward(size)
            turtle.right(angle)

    def star(self, turtle: Turtle, n: int, size: float):
        angle = 180 - 2 * (90 - 360 / n)
        for _ in range(n):
            turtle.forward(size)
            turtle.right(angle)

    pass


SOLUTIONS: List[Base] = [PartA()]
