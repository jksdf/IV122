from Base import Base, AbstractFilenameProvider
from common.turtle.Turtle import Turtle
from week3.common import star, polygon


class PartA(Base):
    name = 'A'

    def run(self, fnprovider: AbstractFilenameProvider):
        fn = fnprovider.get_filename(suffix='.svg', name="shapes")
        turtle = Turtle(fn, (50, 50))
        polygon(turtle, 5, 50)
        turtle.penup()
        turtle.forward(100)
        turtle.pendown()
        star(turtle, 5, 50)
        turtle.penup()
        turtle.forward(100)
        turtle.pendown()
        star(turtle, 7, 50)
        turtle.save(frame=(280, 100))
        return fn