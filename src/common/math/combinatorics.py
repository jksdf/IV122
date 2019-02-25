from collections import Counter
from typing import List, Any, Set, Dict, Tuple, FrozenSet, Callable, Container, Optional


def permutations(data: List[Any]) -> Set[Tuple[Any, ...]]:
    return variations(len(data), data)


def combinations(k: int, data: List[Any]) -> Set[FrozenSet[Any]]:
    return _vc(k, data, frozenset(), lambda elem, prev: frozenset((elem,)).union(prev))


def combinations_repeated(k: int, data: List[Any]) -> List[Dict[Any, int]]:
    if k == 0:
        return [Counter()]
    combs = []
    prev_master = combinations_repeated(k - 1, data)
    for element in data:
        prev = [p.copy() for p in prev_master]
        for p in prev:
            p[element] += 1
        combs += prev
    return combs


def _vc(k: int, data: List[Any], empty, mergefn: Callable[[Any, Container[Any]], Container[Any]]) -> set:
    if k == 0:
        return {empty}
    vc = set()
    for i in range(len(data)):
        prev = _vc(k - 1, data[:i] + data[i + 1:], empty, mergefn)
        vc.update(mergefn(data[i], v) for v in prev)
    return vc


def variations(k: int, data: List[Any]) -> Set[Tuple[Any, ...]]:
    return _vc(k, data, (), lambda elem, prev: (elem,) + prev)


def variations_repeated(k: int, data: List[Any]) -> Set[Tuple[Any, ...]]:
    pass


class PascalTriangle:
    def __init__(self, mod: Optional[int] = None):
        self.data: List[List[Optional[int]]] = [[1]]
        self.mod = mod

    def _get(self, r: int, c: int):
        if self.data[r][c] is None:
            if c == 0 or r == c:
                self.data[r][c] = 1
            else:
                self.data[r][c] = self._get(r - 1, c - 1) + self._get(r - 1, c)
                if self.mod is not None:
                    self.data[r][c] = self.data[r][c] % self.mod
        return self.data[r][c]

    def _fill_rows(self, r: int):
        while len(self.data) <= r:
            self.data.append([None] * (len(self.data) + 1))

    def __getitem__(self, item: slice):
        assert item.step in (1,None)
        assert item.start >= item.stop
        self._fill_rows(item.start)
        return self._get(item.start, item.stop)
