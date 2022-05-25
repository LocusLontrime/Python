# This is the Miller-Rabin test for primes, which works for super large n

import random


def even_odd(n):
    s, d = 0, n
    while d % 2 == 0:
        s += 1
        d >>= 1
    return s, d


def miller_rabin(a, p):
    s, d = even_odd(p-1)
    a = pow(a, d, p)
    if a == 1:
        return True
    for i in range(s):
        if a == p-1:
            return True
        a = pow(a, 2, p)
    return False


def is_prime(p):
    if p == 2:
        return True
    if p <= 1 or p % 2 == 0:
        return False
    return all(miller_rabin(random.randint(2, p - 1), p) for _ in range(55))


print(is_prime(123426017006182806728593424683999798008235734137469123231828679))


