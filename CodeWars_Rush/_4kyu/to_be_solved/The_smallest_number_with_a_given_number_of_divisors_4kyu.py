# accepted on codewars.com
from functools import lru_cache
from math import isqrt

primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43]
rec_counter: int = 0


@lru_cache()
def f(d: int, ind: int = 0) -> int:
    global rec_counter
    rec_counter += 1
    prime_ = primes[ind]                                                      # 36 366 98 989 98989 LL
    res = prime_ ** (d - 1)
    for poss_factor in range(2, isqrt(d) + 1):
        if d % poss_factor == 0:
            f1, f2 = poss_factor, d // poss_factor
            res = min(
                res,
                prime_ ** (f1 - 1) * f(f2, ind + 1),
                prime_ ** (f2 - 1) * f(f1, ind + 1)
            )
    return res


print(f'res -> {f(23 * 7 * 5 * 5 * 3 * 2 * 2 * 2 * 2 * 2 * 2 * 2)}')
# print(f'res -> {f(5 * 3 * 3 * 3 * 2 * 2 * 2 * 2 * 2)}')
print(f'{rec_counter = }')
