from typing import Tuple, Iterable

import numpy as np

from Base import Base, AbstractFilenameProvider
from .PartA import scale, translation, ONE, rotation, shear, square, write, apply, mult


def mrcm(steps: int, lines: Iterable[Tuple[np.ndarray]], newlocs: Iterable[np.ndarray]) -> Iterable[Tuple[np.ndarray]]:
    newlines = []
    for loc in newlocs:
        for line in lines:
            apply()


class PartB(Base):
    name = 'B'

    def run(self, fnprovider: AbstractFilenameProvider):
        return fnprovider.format_files()
