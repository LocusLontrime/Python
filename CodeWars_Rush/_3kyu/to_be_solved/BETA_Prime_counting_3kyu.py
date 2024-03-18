import math
from functools import cache

LIMIT = 13

primes: list[int]
memo_phi: dict[tuple[int, int], int]


def count_primes_less_than(n: int) -> int:
    global primes, memo_phi

    primes = get_primes(1_800_000)
    primes.sort()
    memo_phi = {}

    print(f'size of primes: {len(primes)}')

    return pi(n)


@cache
def pi(n: int) -> int:
    # print(f'{n = }')

    if n <= LIMIT:
        return count(n)
    a = pi(int(pow(n, 1 / 4)))
    b = pi(int(pow(n, 1 / 2)))
    c = pi(int(pow(n, 1 / 3)))

    sum_ = phi(n, a) + (b + a - 2) * (b - a + 1) // 2

    # print(f'{a, b, c = } | {sum_ = }')

    for i in range(a + 1, b + 1):
        w = n // primes[i]
        lim = pi(math.isqrt(w))
        sum_ -= pi(w)
        if i <= c:
            for j in range(i, lim + 1):
                sum_ -= pi(w // primes[j]) - j + 1

    return sum_


def count(n: int) -> int:
    return [0, 0, 1, 2, 2, 3, 3, 4, 4, 4, 4, 5, 5, 6][n]


@cache
def phi(x: int, a: int) -> int:

    res = 0
    while True:
        if not a or not x:
            return x + res

        a -= 1
        res -= phi(x // primes[a], a)  # partial tail recursion


def get_primes(n):  # Eratosthenes' sieve
    """
    param n: max number to which we should build the primes list
    return: list of primes before or equal to n
    """
    # filling the list from 0 to n
    a = []
    for i in range(n + 1):
        a.append(i)
    # 1 is a prime number
    a[1] = 0
    # we begin from 3-rd element
    i = 2
    while i <= n:
        # if the cell value has not yet been nullified -> it keeps the prime number
        if a[i] != 0:
            # the first multiple will be two times larger
            j = i + i
            while j <= n:
                # not a prime -> exchange it with 0
                a[j] = 0
                # proceed to the next number (n % i == 0)
                # it has the value that is larger by i
                j = j + i
        i += 1
    # list to set, all nulls except 1 got removed
    a = set(a)
    # here we delete the last null
    a.remove(0)
    return list(a)


r = count_primes_less_than(666 * 10 ** 8)

print(f'{r = }')









