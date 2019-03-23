import random
from numbers import Real
from typing import List, Tuple

import svgwrite
import svgwrite.shapes

from Base import Base, AbstractFilenameProvider
from common.datagens.lines import gen_line_segments
from common.math.geometry import intersect_linesegments


def intersections(lines: List[Tuple[Tuple[Real, Real], Tuple[Real, Real]]]) -> List[Tuple[Real, Real]]:
    intersects = []
    for i1 in range(len(lines)):
        for i2 in range(i1 + 1, len(lines)):
            intersect = intersect_linesegments(lines[i1], lines[i2])
            if intersect is not None:
                intersects.append(intersect)
    return intersects


class PartA(Base):
    name = 'A'

    def run(self, fnprovider: AbstractFilenameProvider):
        random.seed(433308)
        lines = gen_line_segments(500, 30, (5, 405))
        d = svgwrite.Drawing(fnprovider.get_filename('.svg', 'test', 'Test'), size=(410, 410))
        for start, end in lines:
            d.add(svgwrite.shapes.Line(start, end, stroke='black'))
        for intersection in intersections(lines):
            d.add(svgwrite.shapes.Circle(center=intersection, r=1, stroke='blue'))
        d.save()
        return fnprovider.format_files()
