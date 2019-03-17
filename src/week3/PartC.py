import math

from Base import Base, AbstractFilenameProvider
from common.math.geometry import deg2rad
from common.turtle.Turtle import Turtle


class PartC(Base):
    name = 'C'

    def run(self, fnprovider: AbstractFilenameProvider):
        fn = fnprovider.get_filename(".svg", "fractals")
        turtle = Turtle(fn, (50, 250))
        turtle.left(90)
        self.ker(turtle, 9, size=0.2)
        turtle.resetpos(position=(200, -150))
        turtle.right(60)
        self.sierpinsky(turtle, 5, 9)
        turtle.resetpos(position=(350, -120))
        self.koch(turtle, 5, 0.8)
        turtle.resetpos(position=(600, -150))
        self.hilbert(turtle, 4, 2)
        turtle.resetpos(position=(900, -200))
        self.pentagon(turtle, 3, 10)
        turtle.resetpos(position=(1200, -200))
        self.square_sierpinsky(turtle, 4, 3)
        turtle.save(frame=(1500, 500))
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
