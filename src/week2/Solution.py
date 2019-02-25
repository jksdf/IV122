from collections import namedtuple
from typing import List, Any

import common.math.combinatorics  as combinatorics
from src.Base import Base, AbstractFilenameProvider


class PartA(Base):
    name = 'A'
    comb = namedtuple('Combinatorics',
                      ['permutations', 'combinations', 'combinations_repeated', 'variations', 'variations_repeated'])

    def run(self, fnprovider: AbstractFilenameProvider):
        t = self.combinatorics(3, [1, 2, 3, 4, 5])
        return 'permutations: {}\ncombinations: {}\ncombinations_repeated: {}\nvariations: {}\nvariations_repeated: {}'.format(
            t.permutations, t.combinations, t.combinations_repeated, t.variations, t.variations_repeated)

    def combinatorics(self, k: int, data: List[Any]) -> comb:
        return self.comb(combinatorics.permutations(data), combinatorics.combinations(k, data),
                         combinatorics.combinations_repeated(k, data), combinatorics.variations(k, data),
                         combinatorics.variations_repeated(k, data))


SOLUTIONS: List[Base] = [PartA()]
