# Вычислить число  c заданной точностью d
# Пример: при d = 0.001,  c= 3.141.

def calc_pi_precision_alt(precision: float) -> float:
    pi = 3.0
    i = 2
    while True:
        pi += (-1 if i % 4 == 0 else 1) * 4 / (i * (i + 1) * (i + 2))
        k = abs(4 / (i * (i + 1) * (i + 2)) - 4 / (i + 2 * (i + 3) * (i + 4)))

        print(f'i = {i}, delta = {k}')

        if k < precision:
            return pi
        i += 2


print(calc_pi_precision_alt(0.000001))



