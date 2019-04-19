from common.lsystem.LSystem import LSystem
from common.turtle.Turtle import Turtle


def triangle(fn):
    angle = 120
    length = 10
    turtle = Turtle(fn, (80,250))
    lsystem = LSystem({'F': lambda: turtle.forward(length),
                       'f': lambda: turtle.forward(length, usepen=False),
                       '+': lambda: turtle.right(angle),
                       '-': lambda: turtle.left(angle)},
                      {'F': 'F-F+F'},
                      'F+F+F')
    lsystem.run(0)
    turtle.resetpos((50, 0))
    lsystem.run(1)
    turtle.resetpos((100, 0))
    lsystem.run(2)
    turtle.resetpos((160, 0))
    lsystem.run(3)
    turtle.resetpos((280, 0))
    lsystem.run(4)
    turtle.resetpos((400, 0))
    lsystem.run(5)
    turtle.save(frame=(500,150))


def _stack_pop(turtle, posang):
    turtle.position, turtle.angle = posang


def square_sierpinsky(fn):
    angle = 90
    length = 3
    turtle = Turtle(fn, (10,100))
    turtle.left(90)
    lsystem = LSystem({'F': lambda: turtle.forward(length),
                       'X': lambda: None,
                       '+': lambda: turtle.right(angle),
                       '-': lambda: turtle.left(angle)},
                      {'F': 'F',
                       'X': 'XF-F+F-XF+F+XF-F+F-X'},
                      'F+XF+F+XF')
    lsystem.run(4)
    turtle.save(fn, (200,100))


def cantor(fn, length=300):
    turtle = Turtle(fn, (20, 10))
    lsystem = LSystem({'F': lambda: turtle.forward(length),
                       'f': lambda: turtle.forward(length, usepen=False)},
                      {'F': 'FfF', 'f': 'fff'},
                      'F')

    for i in range(7):
        turtle.resetpos((0, i * 20))
        lsystem.run(i)
        length /= 3
    turtle.save(fn, (350, 100))


def crystal(fn):
    turtle = Turtle(fn,(2,2))
    lsystem = LSystem({'F': lambda: turtle.forward(2),
                       '+': lambda: turtle.right(90)},
                      {'F': 'FF+F++F+F'},
                      'F+F+F+F')

    lsystem.run(5)
    turtle.save(fn, (490,490))
