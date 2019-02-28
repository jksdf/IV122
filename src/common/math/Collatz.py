from typing import List


class Collatz:
    def __init__(self):
        self.mem = {1: 1}

    def get(self, n: int) -> int:
        if n in self.mem:
            return self.mem[n]
        nxt = (n // 2) if n % 2 == 0 else (n * 3 + 1)
        self.mem[n] = 1 + self.get(nxt)
        return self.mem[n]
