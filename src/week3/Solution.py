import math
from typing import List

from src.common.lsystem.Examples import crystal, cantor, square_sierpinsky, weed, triangle
from src.Base import Base, AbstractFilenameProvider
from src.common.math.geometry import deg2rad, rad2deg
from src.common.turtle.Turtle import Turtle


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
        fn = fnprovider.get_filename(suffix='.svg', name="polygon")
        turtle = Turtle(fn)
        self.pentagon(turtle)
        turtle.resetpos(position=(250, 0))
        self.squares(turtle)
        turtle.resetpos(position=(400, 0))
        self.grid(turtle)
        turtle.resetpos(position=(750, 0))
        self.triangles(turtle)
        turtle.resetpos(position=(900, 0))
        self.flower(turtle)
        turtle.save()
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


class PartC(Base):
    name = 'C'

    def run(self, fnprovider: AbstractFilenameProvider):
        fn = fnprovider.get_filename(".svg", "fractals")
        turtle = Turtle(fn)
        turtle.left(90)
        self.ker(turtle, 10)
        turtle.resetpos(position=(200, -150))
        turtle.right(60)
        self.sierpinsky(turtle, 6, 3)
        turtle.resetpos(position=(350, -120))
        self.koch(turtle, 5, 0.8)
        turtle.resetpos(position=(600, -150))
        self.hilbert(turtle, 4, 2)
        turtle.resetpos(position=(900, -200))
        self.pentagon(turtle, 3, 10)
        turtle.resetpos(position=(1200, -200))
        self.square_sierpinsky(turtle, 5, 2)
        turtle.save()
        return fn

    def ker(self, turtle, depth, size=0.1):
        if depth == 0:
            return
        dist = size * 2 ** depth
        turtle.forward(dist)
        turtle.right(30)
        self.ker(turtle, depth - 1)
        turtle.left(60)
        self.ker(turtle, depth - 1)
        turtle.right(30)
        turtle.back(dist)

    def sierpinsky(self, turtle, depth, size=0.1):
        if depth == 0:
            return
        turtle.pendown()
        side = size * 2 ** depth
        for _ in range(3):
            turtle.forward(side)
            turtle.right(120)

        self.sierpinsky(turtle, depth - 1, size)
        turtle.forward(side / 2, usepen=False)
        self.sierpinsky(turtle, depth - 1, size)
        turtle.right(120)
        turtle.forward(side / 2, usepen=False)
        turtle.left(120)
        self.sierpinsky(turtle, depth - 1, size)
        turtle.right(120)
        turtle.back(side / 2, usepen=False)
        turtle.left(120)
        turtle.back(side / 2, usepen=False)

    def koch(self, turtle, depth, size):
        for _ in range(3):
            self.kochline(turtle, depth, size)
            turtle.right(120)

    def kochline(self, turtle: Turtle, depth, size):
        if depth == 1:
            turtle.forward(size * 3 ** depth)
            return
        self.kochline(turtle, depth - 1, size)
        turtle.left(60)
        self.kochline(turtle, depth - 1, size)
        turtle.right(120)
        self.kochline(turtle, depth - 1, size)
        turtle.left(60)
        self.kochline(turtle, depth - 1, size)

    def hilbert(self, turtle: Turtle, depth, size):
        turtle.right(90)
        if depth == 0:
            turtle.forward(size * 3)
            turtle.left(90)
            turtle.forward(size * 3)
            turtle.left(90)
            turtle.forward(size * 3)
            turtle.right(90)
        else:
            innersize = self.hs(depth - 1) * size * 3
            turtle.forward(innersize, usepen=False)
            turtle.right(180)
            self.hilbert(turtle, depth - 1, size)
            turtle.right(180)
            turtle.forward(innersize, usepen=False)
            turtle.forward(size * 3)
            turtle.left(90)
            self.hilbert(turtle, depth - 1, size)
            turtle.forward(size * 3)
            self.hilbert(turtle, depth - 1, size)
            turtle.left(90)
            turtle.forward(size * 3)
            turtle.forward(innersize, usepen=False)
            turtle.right(180)
            self.hilbert(turtle, depth - 1, size)
            turtle.right(180)
            turtle.forward(innersize, usepen=False)
            turtle.right(90)

    def hs(self, n):
        if n == 0:
            return 1
        return 2 * self.hs(n - 1) + 1

    def pentagon(self, turtle: Turtle, depth, size):
        outerangle = 360 / 5
        innerangle = 180 - outerangle
        if depth == 0:
            for _ in range(5):
                turtle.forward(size)
                turtle.right(outerangle)
            return
        for _ in range(5):
            self.pentagon(turtle, depth - 1, size)
            turtle.forward(self.pentsize(depth) * size, usepen=False)
            turtle.right(outerangle)
        prevsize = self.pentsize(depth - 1) * size
        turtle.forward(prevsize, usepen=False)
        turtle.right(outerangle)
        turtle.forward(prevsize, usepen=False)
        turtle.right(outerangle - innerangle)

        self.pentagon(turtle, depth - 1, size)
        turtle.left(outerangle - innerangle)
        turtle.back(prevsize, usepen=False)
        turtle.left(outerangle)
        turtle.back(prevsize, usepen=False)

    def pentsize(self, n):
        if n == 0:
            return 1
        else:
            innerangle = 180 - 360 / 5
            return self.pentsize(n - 1) * (2 + math.sqrt(2 * (1 - math.cos(deg2rad(360 - 3 * innerangle)))))

    def square_sierpinsky(self, turtle, depth, size):
        if depth == 0:
            return
        for _ in range(4):
            turtle.forward(size * 3 ** depth)
            turtle.right(90)
        turtle.forward(size * 3 ** (depth - 1), usepen=False)
        turtle.right(90)
        turtle.forward(size * 3 ** (depth - 1), usepen=False)
        turtle.left(90)
        for _ in range(4):
            turtle.forward(size * 3 ** (depth - 1))
            turtle.right(90)
        turtle.right(90)
        turtle.back(size * 3 ** (depth - 1), usepen=False)
        turtle.left(90)
        turtle.back(size * 3 ** (depth - 1), usepen=False)

        for _ in range(4):
            for _ in range(2):
                self.square_sierpinsky(turtle, depth - 1, size)
                turtle.forward(size * 3 ** (depth - 1), usepen=False)
            turtle.forward(size * 3 ** (depth - 1), usepen=False)
            turtle.right(90)


class PartD(Base):
    """Inspired by http://paulbourke.net/fractals/lsys/"""
    name = 'D'

    def run(self, fnprovider: AbstractFilenameProvider):
        triangle(fnprovider.get_filename('.svg', 'triangle', 'Triangle'))
        weed(fnprovider.get_filename('.svg', 'weed', 'Weed'))
        square_sierpinsky(fnprovider.get_filename('.svg', 'sq_sierp', 'Square Sierpinski'))
        cantor(fnprovider.get_filename('.svg', 'cantor', 'Cantor set'))
        crystal(fnprovider.get_filename('.svg', 'crystal', 'Crystal'))
        return fnprovider.format_files()


SOLUTIONS: List[Base] = [PartA(), PartB(), PartC(), PartD()]
