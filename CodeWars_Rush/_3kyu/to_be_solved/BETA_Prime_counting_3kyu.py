import math


def count_primes_less_than(n: int) -> int:
    #Your code here
    return 0


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
    return a










