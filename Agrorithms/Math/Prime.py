import time

import gmpy2


def prime_ant(n):
    a = [*range(2, 2 + n)]
    p = 0
    primes = []
    for i in range(n):
        if gmpy2.is_prime(a[p]):
            p += 1
        else:
            q, r = 0, a[p]
            for q in primes:
                if r % q == 0: break
            if q == 0 or r % q != 0:
                while r % (q := gmpy2.next_prime(q)) != 0:
                    primes.append(int(q))
            a[p] //= q
            a[p - 1] += q
            p -= 1
    return a[:p + 1]


start = time.time_ns()
print(prime_ant(1000000))
end = time.time_ns()
print(f'Time elapsed: {(end - start) // 10 ** 6} milliseconds')

