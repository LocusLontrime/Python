# Вычислить число  c заданной точностью d
# Пример: при d = 0.001,  c= 3.141.
from decimal import Decimal
from decimal import getcontext


getcontext().prec = 25


def calc_pi_precision_alt(precision: float) -> float:  # not co fast converges
    pi = 3.0
    i = 2
    delta = 1
    while True:
        prev_delta = delta
        delta = (-1 if i % 4 == 0 else 1) * 4 / (i * (i + 1) * (i + 2))
        pi += delta
        k = abs(prev_delta - delta)
        print(f'i = {i}, pi = {pi}, current delta = {k}')
        if k < precision:
            return pi
        i += 2


getcontext().prec = 350


def newton_arcsine_series(precision: Decimal) -> Decimal:  # converges almost instantly
    pi = Decimal(1 / 2)
    delta = Decimal(1 / 2)
    i = 1
    while True:
        prev_delta = delta
        delta *= (2 * i - 1) ** 2
        delta /= (2 * i)
        delta /= (2 * i + 1)
        delta /= 4
        pi += delta
        print(f'iteration: {i}, pi = {6 * pi}, current delta = {delta}')
        if abs(prev_delta - delta) < precision:
            return 6 * pi
        i += 1


print(calc_pi_precision_alt(0.00000001))
print(newton_arcsine_series(Decimal(1/10**300)))  # precision of a default Decimal type is out of range for such calculations...



