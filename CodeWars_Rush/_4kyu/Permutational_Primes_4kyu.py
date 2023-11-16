# accepted on codewars.com
from collections import defaultdict as d, Counter
from bisect import bisect_left
import time

primes = None
perm_primes = d(list)
perms = {}
PRIMES_THRESHOLD = 1_000_000
middle: int


def permutational_primes(n_max, k_perms):  # 36 366 98 989
    global primes, perm_primes, middle
    print(f'n max: {n_max}, k perms: {k_perms}')
    if primes is None:
        primes = list(sorted(get_primes(PRIMES_THRESHOLD)))
        # print(f'primes: {primes}')
        for prime in primes:
            counter_ = Counter(f'{prime}')
            keys_sorted = sorted(counter_.keys())
            perm_primes[' '.join([f'{key_}:{counter_[key_]}' for key_ in keys_sorted])].append(prime)
        # print(f'dict_: ')
        for k, v in perm_primes.items():
            perms[v[0]] = v
            # print(f'{k} -> {v}')
        del perm_primes
        # for k, v in perms.items():
        #     print(f'{k} -> {v}')
        print(f'perms length: {len(primes)}')
    middle = time.time_ns()
    counter = 0
    such_primes = []
    for k, v in perms.items():
        if k > n_max:
            break
        inner_counter = bisect_left(v, n_max)
        # print(f'k, inner_counter, k_perms: {k, inner_counter, k_perms}')
        if inner_counter - 1 == k_perms:
            counter += 1
            such_primes.append(k)
    print(f'such_primes: {such_primes}')
    return [counter, such_primes[0], such_primes[-1]] if such_primes else [0, 0, 0]


def get_primes(n: int) -> set[int]:  # Eratosthenes' sieve
    """
    :param n: max number to which we should build the primes list
    :return: list of primes before or equal to n
    """
    # filling the list from 0 to n
    a = []
    for i in range(n + 1):
        a.append(i)
    # 1 is a prime number
    a[1] = 0
    # we begin from 3-th element
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
    return a


start = time.time_ns()
print(f'res: {permutational_primes(1_000_000, 101)}')  # 3, 149, 379
# print(permutational_primes(29999, 11))
finish = time.time_ns()
print(f'time elapsed for primes list built: {(middle - start) // 10 ** 6} milliseconds')
print(f'time elapsed for further calcs: {(finish - middle) // 10 ** 6} milliseconds')










                                                                                        # 36 366 98 989 98989 LL