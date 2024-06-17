# accepted on codewars.com -> very fast...
import math
import time
from random import randint
from collections import defaultdict as defd


MR_THRESHOLD = 5  # only for Miller-Rabin check


def two_squares(n: int):
    print(f'{n = }')

    # let us factorize n:
    prime_factors = factorize(n)

    # checks if number n is representable as 2 squares:
    two_sq_representable = all(prime_factors[p] % 2 == 0 or if_quadrifyable(p) for p in prime_factors.keys())

    if not two_sq_representable:
        # if not -> returns 0...
        return 0

    # calculates common multiple (even powers of prime factors 4 * k + 3)
    sq_multiplier = 1
    for p, power in prime_factors.items():
        if not if_quadrifyable(p):
            sq_multiplier *= p ** (power // 2)

    # builds list of all factors remained (only quadrifyable factors counted):
    factors = []
    for p, power in prime_factors.items():
        if if_quadrifyable(p):
            factors += [p for _ in range(power)]
    factors.sort()

    # the main cycle (gets the final 2 square decomposition):
    pairs = [(1, 0)]  # means One...
    for factor in factors:
        # quadrifying of the current factor:
        pair_ = find_quadratic_pair(factor)
        new_pairs = []
        # simplifying equations like (a^2 + b^2) * (c ^ 2 + d ^ 2) into -> x^2 + y^2
        for pair in pairs:
            new_pairs += (r := simplify(*pair, *pair_))
        pairs = new_pairs

    # defines the best squares:
    best_pair = max(pairs, key=lambda p: p[0] + p[1])

    # returns the sum of them (do not forget about already computed common multiple):
    return sq_multiplier * sum(best_pair)


def find_quadratic_pair(prime: int) -> tuple[int, int]:
    """quadrifies the prime given: prime = x^2 + y^2"""
    x = 1
    while x ** 2 <= prime // 2 + 1:
        if (y := math.isqrt(rem := prime - x ** 2)) ** 2 == rem:
            return x, y
        x += 1


def simplify(a: int, b: int, c: int, d: int) -> list[tuple[int, int]]:
    """simplifies (a^2 + b^2) * (c^2 + d^2) to x^2 + y^2"""
    x1, y1 = a * c + b * d, abs(a * d - b * c)
    x2, y2 = abs(a * c - b * d), a * d + b * c
    return [(x1, y1), (x2, y2)]


def if_quadrifyable(p: int) -> bool:
    """checks if the prime number p can be quadrified"""
    return p == 2 or p % 4 == 1


# brent from stackoverflow or smth similar...
def brent(n: int):
    """fast algorithm for finding a non-trivial factor of n"""
    if n % 2 == 0:
        return 2
    y, c, m = randint(1, n - 1), randint(1, n - 1), randint(1, n - 1)
    g, r, q = 1, 1, 1
    while g == 1:
        x = y
        for i in range(r):
            y = ((y * y) % n + c) % n
        k = 0
        while k < r and g == 1:
            ys = y
            for i in range(min(m, r - k)):
                y = ((y * y) % n + c) % n
                q = q * (abs(x - y)) % n
            g = math.gcd(q, n)
            k = k + m
        r = r * 2
    if g == n:
        while 1:
            ys = ((ys * ys) % n + c) % n
            g = math.gcd(abs(x - ys), n)
            if g > 1:
                break
    return g


def factorize(n: int) -> defd[int, int]:
    """fast factorization method based on Brent's Pollard Rho algorithm"""

    MAX_ = 1_000  # approx const...

    factors = defd(int)

    temp = n

    # 2 and 3 primes:
    while n % 2 == 0:
        factors[2] += 1
        n //= 2

    while n % 3 == 0:
        factors[3] += 1
        n //= 3

    # little divisors:
    i = 5
    inc = 2
    while i <= MAX_:
        while n % i == 0:
            factors[i] += 1
            n //= i
        i += inc
        inc = 6 - inc

    # big ones:
    while n > 1 and not is_prime(n):
        divisor = n
        while not is_prime(divisor := brent(divisor)):
            ...
        while n % divisor == 0:
            factors[divisor] += 1
            n //= divisor
    if n > 1:
        factors[n] += 1  # 36 366 98 989 98989 LL

    return factors


# Miller-Rabin prime test section ->
def get_pars(n):
    power, multiplier = 0, n
    while multiplier % 2 == 0:
        power += 1
        multiplier >>= 1
    return power, multiplier


def miller_rabin_test(a, p):
    power, multiplier = get_pars(p - 1)
    a = pow(a, multiplier, p)
    if a == 1:
        return True
    for i in range(power):
        if a == p - 1:
            return True                                                               # 36 366 98 989 98989 LL
        a = pow(a, 2, p)
    return False


def is_prime(p):
    """checks if number p is prime"""
    if p == 2:
        return True
    if p <= 1 or p % 2 == 0:
        return False
    return all(miller_rabin_test(randint(2, p - 1), p) for _ in range(MR_THRESHOLD))


# n_ = 1365584311572932090993  # -> 52251808985
number = 1365584311572932090993  # 78400


num = 1180591620717411303424

start = time.time_ns()
print(f'res: {two_squares(number)}')
finish = time.time_ns()
print(f'time elapsed: {(finish - start) // 10 ** 6} milliseconds')


