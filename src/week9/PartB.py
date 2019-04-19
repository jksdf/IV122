from collections import Counter
from typing import Dict, List

import matplotlib.pyplot as plt

from Base import Base, AbstractFilenameProvider


def subs(k, n):
    if n == 0:
        return [()]
    lower = subs(k, n - 1)
    return [(v,) + l for v in range(1, k + 1) for l in lower]


class PartB(Base):
    name = 'B'

    def analyze(self, ln, fn) -> Dict[int, int]:
        with open(fn) as f:
            vals = tuple(map(int, filter(None, f.read().split())))
            c = Counter()
            for idx in range(len(vals) - ln):
                c[vals[idx:idx + ln]] += 1
            return c

    def render(self, ln, fns: List[str]):
        f, axarr = plt.subplots(len(fns), figsize=(10, 10))
        f.suptitle(f'Distributions of {ln}-grams')
        vals = subs(6, ln)
        vals_str = list(map(str, vals))
        for idx in range(len(fns)):
            analysis = self.analyze(ln, fns[idx])
            y = [analysis[p] for p in vals]
            axarr[idx].set_title(fns[idx])
            axarr[idx].bar(vals_str, y, 1)
        f.subplots_adjust(hspace=0.5)
        f.autofmt_xdate()
        return f

    def run(self, fnprovider: AbstractFilenameProvider):
        files = [f'../resources/w9/random{f}.txt' for f in range(1, 8)]
        for i in range(1, 5):
            self.render(i, files).savefig(fnprovider.get_filename(".png", f"{i}-grams", f"{i}-grams"))
        return fnprovider.format_files()
