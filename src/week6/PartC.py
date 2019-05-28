from Base import Base, AbstractFilenameProvider
from common.lsystem.LSystem import LSystem
from common.turtle.Turtle import Turtle


def weed(fn):
    turtle = Turtle(fn, (10, 500))
    turtle.left(90)
    lsystem = LSystem('X',
                      {'X': 'F+[[X]-X]-F[-FX]+X', 'F': 'FF'})
    turtle.resetpos((50, 0), -90)
    lsystem.run(turtle, 1, 6, 25, thickness='sq')
    turtle.resetpos((100, 0), -90)
    lsystem.run(turtle, 2, 6, 25, thickness='sq')
    turtle.resetpos((150, 0), -90)
    lsystem.run(turtle, 3, 6, 25, thickness='sq')
    turtle.resetpos((200, 0), -90)
    lsystem.run(turtle, 4, 6, 25, thickness='sq')
    turtle.resetpos((300, 0), -90)
    lsystem.run(turtle, 5, 6, 25, thickness='sq')
    turtle.save(fn, frame=(480, 20))


def koch(fn):
    turtle = Turtle(fn, (50, 50))
    turtle.left(90)
    lsystem = LSystem('F--F--F',
                      {'F': 'F+F--F+F'})
    turtle.resetpos((100, 150), -90)
    lsystem.run(turtle, depth=3, step=6, angle=60)
    turtle.save(fn, frame=(200, 200))


def sierpinsky(fn, angle=60, step=6):
    turtle = Turtle(fn, (50, 50))
    turtle.left(90)
    lsystem = LSystem('A',
                      {'A': 'B-A-B',
                       'B': 'A+B+A'})
    turtle.resetpos((400, 400), 180)
    lsystem.run(turtle, depth=6, step=step, angle=angle)
    turtle.save(fn, frame=(500, 550))


def paprad(fn):
    """Attributed to Saupe"""
    turtle = Turtle(fn, (50, 50))
    turtle.left(90)
    lsystem = LSystem('VZFFF',
                      {'V': '[+++W][---W]YV',
                       'W': '+X[-W]Z',
                       'X': '-W[+X]Z',
                       'Y': 'YZ',
                       'Z': '[-FFF][+FFF]F'})
    turtle.resetpos((200, 400), -90)
    lsystem.run(turtle, depth=8, step=8, angle=20, thickness='sq')
    turtle.save(fn, frame=(500, 550))


def pentaplexity(fn):
    """By: Paul Bourke"""
    turtle = Turtle(fn, (50, 50))
    turtle.left(90)
    lsystem = LSystem('F++F++F++F++F',
                      {'F': 'F++F++F|F-F++F'})
    turtle.resetpos((80,0), 0)
    lsystem.run(turtle, depth=4, step=8, angle=36)
    turtle.save(fn, frame=(600, 600))
    pass


class PartC(Base):
    name = 'C'

    def run(self, fnprovider: AbstractFilenameProvider):
        weed(fnprovider.get_filename('.svg', 'weed_growth', 'Weed growth'))
        koch(fnprovider.get_filename('.svg', 'koch', 'Koch'))
        sierpinsky(fnprovider.get_filename('.svg', 'sierpinsky', "Sierpinsky"))
        sierpinsky(fnprovider.get_filename('.svg', 'sierpinsky_twisted', "Sierpinsky twisted"), angle=56, step=4)
        paprad(fnprovider.get_filename('.svg', 'paprad', 'Paprad'))
        pentaplexity(fnprovider.get_filename('.svg', 'pentaplexity', "Pentaplexity"))

        return fnprovider.format_files()
