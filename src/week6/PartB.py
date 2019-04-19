from typing import List, Tuple

from PIL import Image

from Base import Base, AbstractFilenameProvider


def avg(lst):
    return sum(lst) / len(lst)


def logisticMap(x0: float, r: float, drop: int = 100, sample: int = 100, epsilon: float = 0.01) -> List[float]:
    x = x0
    for _ in range(drop):
        x = r * x * (1 - x)
    vals = []
    for _ in range(sample):
        x = r * x * (1 - x)
        vals.append(x)
    return vals


def bifurcations(rRange: Tuple[float, float], rCount: int, xRange: Tuple[float, float], xCount: int, x0: float):
    img = Image.new("1", (rCount, xCount), 1)
    for ridx in range(rCount):
        r = (rRange[1] - rRange[0]) * ridx / rCount + rRange[0]
        for x in logisticMap(x0, r):
            xidx = int((x - xRange[0]) / (xRange[1] - xRange[0]) * xCount)
            img.putpixel((ridx, xidx), 0)
    return img


class PartB(Base):
    name = 'B'

    def run(self, fnprovider: AbstractFilenameProvider):
        bifurcations((2, 4), 10000, (0, 1), 5000, .2).save(fnprovider.get_filename('.png', 'bif', 'Bifurcations'))
        return fnprovider.format_files()

    pass
