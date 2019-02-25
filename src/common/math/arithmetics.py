def pow(base: float, power: int, modulo: int):
    ongoing = 1
    exp = base % modulo
    while power != 0:
        if power % 2 == 1:
            ongoing = (ongoing * exp) % modulo
        power = power // 2
        exp = (exp * exp) % modulo
    return ongoing


def pow_naive(base: float, power: int, modulo: int):
    tmp = 1
    for _ in range(power):
        tmp = (tmp * base) % modulo
    return tmp
