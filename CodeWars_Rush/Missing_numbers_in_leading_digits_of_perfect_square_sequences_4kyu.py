# accepted on codewars.com (beta)
import math


def sqrt_even(power):
    return int(math.isqrt(10 ** power)) + 1


def missing_number(x):
    if x >= 5:
        return int('25' + ('0' * (k := x // 2 - 2) + str(sqrt_even(x)) if x % 2 == 1 else '0' * (x // 2 - 3) + '1' + '0' * (x // 2)))
    else:
        return [2, 5, 35, 282, 2600][x]


print(missing_number(5))
print(missing_number(11))
print(missing_number(12))

