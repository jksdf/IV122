from typing import List, Any, Set, Dict, Tuple, FrozenSet, Callable, Collection, Container
from collections import Counter


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

def variations_repeated(k:int, data:List[Any]) -> Set[Tuple[Any, ...]]:
    pass
