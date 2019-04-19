from typing import Dict, List

from common.turtle.Turtle import Turtle


class LSystem:
    def __init__(self, axiom: str, rules: Dict[str, str], constants='[]+-'):
        self.axiom = axiom if type(axiom) == list else list(axiom)
        self.rules: Dict[str, List[str]] = {k: list(v) for k, v in rules.items()}
        for constant in constants:
            self.rules[constant] = [constant]

    def run(self, turtle: Turtle, depth: int, step: float, angle: float = 90, thickness='constant'):
        s = self.generate_string(depth)
        stack = []
        for i in s:
            if i == '[':
                stack.append((turtle.position, turtle.angle))
            elif i == ']':
                turtle.position, turtle.angle = stack.pop()
            elif i == '+':
                turtle.right(angle)
            elif i == '-':
                turtle.left(angle)
            elif i == 'f':
                turtle.forward(step, usepen=False)
            elif i == 'F':
                turtle.forward(step, usepen=True, thickness=1.5/(len(stack)+1)**0.5 if thickness else 1)
            elif i.isalpha():
                pass
            else:
                raise ValueError("Incorrect action")

    def generate_string(self, depth: int) -> List[str]:
        s = self.axiom
        for _ in range(depth):
            next_s = []
            for i in s:
                next_s += self.rules[i] if i in self.rules else i
            s = next_s
        return s
