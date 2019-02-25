from typing import Callable, List


def sample(function: Callable[[], float], times: int,
           avg: Callable[[List[float]], float] = lambda lst: sum(lst) / len(lst)):
    samples = [function() for _ in range(times)]
    return avg(samples)
