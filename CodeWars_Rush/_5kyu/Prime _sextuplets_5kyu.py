# accepted on codewars.com
SIZE = 6
ADDINGS = [0, 4, 6, 10, 12, 16]
PRIMES = []
MAX_PRIME = 6_200_000
from bisect import bisect_left


def find_primes_sextuplet(sum_limit):  # 36 366 98 989 98989
    global PRIMES
    if not PRIMES:
        PRIMES = get_primes(MAX_PRIME)
    _p = (sum_limit - sum(ADDINGS)) // SIZE
    print(f'_p: {_p}')
    pi = bisect_left(PRIMES, _p)
    while True:
        for i, add_ in enumerate(ADDINGS):
            if PRIMES[pi + i] != PRIMES[pi] + add_:
                break
        else:
            return [PRIMES[pi] + add_ for add_ in ADDINGS]
        pi += 1


def get_primes(n: int):  # Eratosthenes' sieve
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
    return list(sorted(a))


n_ = 1091257
# print(f'prime or not: {fermi_test(n_)}')

print(f'res: {find_primes_sextuplet(2_000_000)}')

# print(f'primes: {(pr := get_primes(6_200_000))}')
# p = 17
# print(f'index of ({p}): {bisect_left(pr, p)}')

