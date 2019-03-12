from typing import Dict, Callable

from common.turtle.Turtle import Turtle


class LSystem:
    def __init__(self, alphabet: Dict[str, Callable[[], None]], rules: Dict[str, str], axiom: str):
        assert all(len(k) == 1 for k in alphabet.keys())
        # assert all(k in rules.keys() for k in alphabet.keys())
        assert all(len(k) == 1 for k in rules.keys())
        assert all(k in alphabet.keys() for k in axiom)
        self.alphabet = alphabet
        self.rules = {k:list(v) for k,v in rules.items()}
        self.axiom = list(axiom)

    def run(self, depth: int):
        s = self._get_string(depth)
        for i in s:
            self.alphabet[i]()

    def _get_string(self, depth:int):
        s = self.axiom
        for _ in range(depth):
            next_s = []
            for i in s:
                next_s += self.rules[i] if i in self.rules else i
            s = next_s
        return s




