import numpy as np
from itertools import combinations as combs


def f(d: int) -> int:

    prime_factors = get_prime_factors(d)

    return 0


def get_prime_factors(n):
    num = n
    index = 0
    factors_candidates = [2, 3, 5, 7]
    factors = []
    while factors_candidates[index] ** 2 <= n:
        if len(factors_candidates) == index + 1:
            factors_candidates.append(factors_candidates[-2] + 6)
        if n % factors_candidates[index]:
            index += 1
        else:
            n //= factors_candidates[index]
            factors.append(factors_candidates[index])
    if n > 1:
        factors.append(n)
    return factors


print(f(1000000))
print(list(combs(range(5), 3)))


