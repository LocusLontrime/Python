# Вычислить число  c заданной точностью d
# Пример: при d = 0.001,  c= 3.141.

def calc_pi_precision_alt(precision: float) -> float:  # not co fast converges
    pi = 3.0
    i = 2
    while True:
        pi += (-1 if i % 4 == 0 else 1) * 4 / (i * (i + 1) * (i + 2))
        k = abs(4 / (i * (i + 1) * (i + 2)) - 4 / (i + 2 * (i + 3) * (i + 4)))

        print(f'i = {i}, delta = {k}')

        if k < precision:
            return pi
        i += 2


def newton_arcsine_series(precision: float) -> float:  # converges almost instantly
    pi = 1 / 2
    delta = 1 / 2
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


print(calc_pi_precision_alt(0.000001))
print(newton_arcsine_series(0.000000000001))



