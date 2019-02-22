import bisect


class Fibonacci:
    def __init__(self):
        self.data = [1, 1]

    def goto(self, n: int):
        """Calculates fib sequence to at least n."""
        while self.data[-1] < n:
            self.data.append(self.data[-1] + self.data[-2])

    def __contains__(self, item: int):
        self.goto(item)
        res = bisect.bisect_left(self.data, item)
        return res != len(self.data) and self.data[res] == item
