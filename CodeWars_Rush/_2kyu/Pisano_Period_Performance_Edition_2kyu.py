# accepted on codewars.com
from random import randint
import math
import time
from collections import defaultdict as d


MR_THRESHOLD = 5  # only one Miller-Rabin check


# brent from stackoverflow or smth similar...
def brent(n: int):
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


def factorize(n: int) -> d[int, int]:
    MAX_ = 1_000  # approx const...

    factors = d(int)
    print(f'factorization of {n}:')

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
    print(f'starting brent for {n}')
    while n > 1 and not is_prime(n):
        print(f'...{n = }')
        divisor = n
        while not is_prime(divisor := brent(divisor)):
            ...
        while n % divisor == 0:
            factors[divisor] += 1
            n //= divisor
    if n > 1:
        factors[n] += 1  # 36 366 98 989 98989 LL

    print(f'...{temp} factorization -> {factors}')
    return factors


# Miller-Rabin prime test section
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
    if p == 2:
        return True
    if p <= 1 or p % 2 == 0:
        return False
    return all(miller_rabin_test(randint(2, p - 1), p) for _ in range(MR_THRESHOLD))


def pisano_period(n: int) -> int:
    memo_table = {1: 1, 2: 3, 3: 8, 5: 20}

    def _pisano_period(n_: int) -> int:

        print(f'{n_ = }')

        if n_ not in memo_table.keys():

            if not is_prime(n_):
                # here we use the property of pisano period -> If m and n are coprime, then k(mn) = lcm(k(m), k(n))
                # at first, let us find the divisor of n with Pollard rho factorization algo:
                n_temp, q = n_, 0
                # Brent's method rarely gives some wrong prime factors (compound ones)...
                divisor = n_
                while not is_prime(divisor := brent(divisor)):
                    ...

                while n_temp % divisor == 0:
                    n_temp, q = n_temp // divisor, q + 1

                print(f'{divisor} divisor of {n} found!')
                # then apply the property:
                memo_table[n_] = math.lcm(divisor ** (q - 1) * _pisano_period(divisor), _pisano_period(n_ // divisor ** q))

            else:
                # pisano periods has some more good properties:
                # If n_ > 5 is a prime and n_ = +-1 (mod5) then k(n_) is a divisor of n_ - 1:
                if n_ % 5 in [1, 4]:
                    memo_table[n_] = find_exact_pisano_period(n_ - 1, n_)
                    # If n_ > 5 is a prime and n_ = +-2 (mod5) then k(n_) is a divisor of 2(n_ + 1):
                elif n_ % 5 in [2, 3]:
                    memo_table[n_] = find_exact_pisano_period(2 * (n_ + 1), n_)

        return memo_table[n_]

    return _pisano_period(n)


def find_exact_pisano_period(k_multiple: int, n: int) -> int:  # performance bottleneck...
    print(f'finding exact pisano_period: {k_multiple, n = }')
    # firstly, we need to factorize k_multiple, using Pollard rho factorization algo:
    factors = factorize(k_multiple)
    # now with recursion we can get all the divisors sorted:
    divisors = []
    print(f'permutations is being built: ')
    rec_permuts(0, factors, 1, divisors)
    divisors.sort()
    print(f'{divisors = }')
    # now we should find the least divisor with property: Fib(d) = Fib(0) (modm) and Fib(d + 1) = Fib(1) (modm)
    for divisor in divisors:
        print(f'current div: {divisor}')
        # check:
        if dijkstra_fib_mod(divisor, n) == 0 and dijkstra_fib_mod(divisor + 1, n) == 1:
            print(f'{divisor} fib modulo divisor is found!!!')
            return divisor


def dijkstra_fib_mod(num: int, modulo: int) -> int:
    memo_table = {}

    def _dijkstra_fib_mod(num_: int) -> int:
        # print(f'{num_ = }')

        if num_ < 3:
            return [0, 1, 1][num_]

        if num_ not in memo_table.keys():
            if num_ % 2:
                n = num_ // 2 + 1
                memo_table[num_] = (_dijkstra_fib_mod(n - 1) ** 2 + _dijkstra_fib_mod(n) ** 2) % modulo
            else:
                n = num_ // 2
                memo_table[num_] = ((2 * _dijkstra_fib_mod(n - 1) + _dijkstra_fib_mod(n)) * _dijkstra_fib_mod(n)) % modulo

        return memo_table[num_]

    res = _dijkstra_fib_mod(num)
    print(f'...calculated FIB({num}) = {res}')
    print(f'...memo table size: {len(memo_table)}')
    return res


def rec_permuts(prev_pf: int, prime_factors: d[int, int], divisor_: int, divisors_: list[int]):
    # adding divisor to divisors:
    divisors_.append(divisor_)
    # body of rec:
    for prime_factor in prime_factors.keys():
        if prime_factor >= prev_pf and prime_factors[prime_factor]:
            prime_factors[prime_factor] -= 1
            rec_permuts(prime_factor, prime_factors, divisor_ * prime_factor, divisors_)
            prime_factors[prime_factor] += 1


# Driver function
if __name__ == "__main__":
    start = time.time_ns()
    number = 1000000007 * 1000000007 * 164344833683972779 * 10160378359708299757  # 50550  # 164344833683972779  # 12348  # 10160378359708299757  # 2438389198053  # 1818176898  # 1048576  # 97240  # 5781481422738353023  # 241352627  # 924579049  # 1150327153  # 2754003367  # 1303172509  # 3134333507  # 4909015607083012303  # 10420707937356172139  # 4951130183589719131  # 5159146749091023589  # 2136247641713586911  # 10223948831677521313  # 2996814036509449019  # 2015759243216495053  # 2806901077363576969  # 13050411083573536069  # 1818176898  # 2438389198053  # 2438389198053
    # print(f'res: {is_prime(1105)}')  # 9746347772161
    # factorize(number)
    print(f'pisano period of ({number}): {(pp := pisano_period(number))}')
    print(f'partial coeff: {"%.10f" % (pp / number)}')
    # print(f'res: {[brent(99) for _ in range(100)]}')
    # dijkstra_fib(1_000_000)
    # print(f'res: {fib_steps(0, 1, 36_665)}')
    finish = time.time_ns()
    print(f'time elapsed: {(finish - start) // 10 ** 6} milliseconds')

# at first, we need to find all the prime factors of n (let's use Pollard rho factorization algo):
#     factors = factorize(n)
