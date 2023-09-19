# accepted on codewars.com, optimized a lot...
import math
from bisect import bisect_left


THRESHOLD = 1_500_000
primes = None


def solve(x: int, y: int) -> int:  # p = 2^m * 3^n + 1
    global primes
    if primes is None:
        max_m, max_n = int(math.log(THRESHOLD, 2)), int(math.log(THRESHOLD, 3))
        bridge_primes = set()
        for m in range(max_m):
            for n in range(max_n):
                p = 2 ** m * 3 ** n + 1
                if is_prime(p) and p <= THRESHOLD:
                    bridge_primes.add(p)
        primes = list(sorted(bridge_primes))
    return bisect_left(primes, y) - bisect_left(primes, x)


def is_prime(a: int) -> bool:
    if a % 2 == 0:
        return a == 2
    d = 3
    while d * d <= a and a % d != 0:
        d += 2
    return d * d > a


print(f'RES: {solve(1000000, 1500000)}')




