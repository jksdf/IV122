from common.turtle.Turtle import Turtle


def star(turtle: Turtle, n: int, size: float):
    angle = 180 - 2 * (90 - 360 / n)
    for _ in range(n):
        turtle.forward(size)
        turtle.right(angle)


def polygon(turtle: Turtle, n: int, size: float):
    angle = 360 / n
    for _ in range(n):
        turtle.forward(size)
        turtle.right(angle)