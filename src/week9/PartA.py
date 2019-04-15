from collections import Counter
from typing import Dict, List
import matplotlib.pyplot as plt

from Base import Base, AbstractFilenameProvider


class PartA(Base):
    name = 'A'

    def analyze(self, ln, fn) -> Dict[int, int]:
        with open(fn) as f:
            vals = tuple(map(int, filter(None, f.read().split())))
            c = Counter()
            for idx in range(len(vals) - ln):
                c[vals[idx:idx + ln]] += 1
            return c

    def render(self, analysis: List[Dict[int, int]]):
        f, axarr = plt.subplots(len(analysis), sharex=True, sharey=True)
        f.suptitle('Distributions')
        for idx in range(len(analysis)):
            axarr[idx].histogram()
        pass

    def run(self, fnprovider: AbstractFilenameProvider):
        pass
