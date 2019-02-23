import math
from typing import Generator


def divisor_count(n: int) -> int:
    divs = 0
    for i in range(1, int(math.sqrt(n)) + 1):
        if n % i == 0:
            divs += 1
    divs = 2 * divs - (1 if int(math.sqrt(n)) ** 2 == n else 0)
    return divs


def isprime(n: int) -> bool:
    for i in range(1, int(math.sqrt(n))):
        i += 1
        if n % i == 0:
            return False
    return True


def genprimes() -> Generator[int, None, None]:
    n = 2
    while True:
        while not isprime(n):
            n += 1
        yield n
        n += 1


def gcd_mod(a: int, b: int) -> int:
    count = 0
    while True:
        if a < b:
            a, b = b, a
        if b == 0:
            return count
        a, b = b, a % b
        count += 1


def gcd_sub(a: int, b: int) -> int:
    count = 0
    while True:
        if a < b:
            a, b = b, a
        if a == b:
            return count
        a, b = a - b, b
        count += 1
