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


class PartC(Base):
    name = 'C'

    def run(self, fnprovider: AbstractFilenameProvider):
        weed(fnprovider.get_filename('.svg', 'weed_growth', 'Weed growth'))

        return fnprovider.format_files()
