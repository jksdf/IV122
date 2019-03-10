import time
from typing import Callable, List


def sample(function: Callable[[], float], intervalns: int):
    target = time.perf_counter_ns() + intervalns
    k = 0
    while time.perf_counter_ns() < target:
        function()
        k += 1
    return k
