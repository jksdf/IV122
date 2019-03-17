import math

from Base import Base, AbstractFilenameProvider
from common.math.geometry import deg2rad, rad2deg
from common.turtle.Turtle import Turtle
from week3.common import star, polygon


class PartB(Base):
    name = 'B'

    def run(self, fnprovider: AbstractFilenameProvider):
        fn = fnprovider.get_filename(suffix='.svg', name="polygon")
        turtle = Turtle(fn)
        self.pentagon(turtle)
        turtle.resetpos(position=(250, 0))
        self.squares(turtle)
        turtle.resetpos(position=(400, 0))
        self.grid(turtle)
        turtle.resetpos(position=(750, 0))
        self.triangles(turtle)
        turtle.resetpos(position=(900, 50))
        self.flower(turtle)
        turtle.save(frame=(1000, 200))
        return fn

    def pentagon(self, turtle):
        turtle.pendown()
        angle = 180 - 360 / 5
        star(turtle, 5, math.sqrt(2 * 100 * 100 - 2 * 100 * 100 * math.cos(deg2rad(angle))))  # cosine rule
        turtle.left((180 - angle) / 2)
        polygon(turtle, 5, 100)
        turtle.right((180 - angle) / 2)
        turtle.penup()

    def squares(self, turtle, iters=50, size=100, offset=0.15):
        turtle.pendown()
        angle = rad2deg(math.atan(offset / (1 - offset)))
        for _ in range(iters):
            for _ in range(4):
                turtle.forward(size)
                turtle.right(90)
            turtle.forward(offset * size)
            turtle.right(angle)
            size = size * (1 - offset)

    def grid(self, turtle, density=10, r=100):
        pos = turtle.position[0] + r, turtle.position[1] + r

        for x in range(-density, density):
            xpos = x * r / density
            ypos = math.sqrt(r ** 2 - xpos ** 2)
            turtle.line(start=(pos[0] + xpos, pos[1] + ypos), end=(pos[0] + xpos, pos[1] - ypos))
            turtle.line(start=(pos[0] + ypos, pos[1] + xpos), end=(pos[0] - ypos, pos[1] + xpos))

    def triangles(self, turtle, side=200, step=17):
        angle = 120
        turtle.pendown()
        turtle.right(60)
        while side > 0:

            for _ in range(3):
                turtle.forward(side)
                turtle.right(angle)
            turtle.right(30)
            turtle.penup()
            turtle.forward(step / 2 / math.cos(deg2rad(30)))
            turtle.pendown()
            turtle.left(30)
            side -= step

    def flower(self, turtle: Turtle):
        for _ in range(12):
            for _ in range(12):
                turtle.forward(20)
                turtle.right(360 / 12)
            turtle.right(360 / 12)