# accepted on codewars.com -->> very fast
import time


carmichael_numbers = {561, 1105, 1729, 2465, 2821, 6601, 8911, 10585, 15841, 29341, 41041, 46657, 52633, 62745, 63973,
                      75361, 101101, 115921, 126217, 162401, 172081, 188461, 252601, 278545, 294409, 314821, 334153,
                      340561, 399001, 410041, 449065, 488881, 512461}
MAX_NUMBER = 500_000


def prime_maxlength_chain(n: int):
    # dict of sets:
    d: dict[int, set[int]] = {1: set()}
    # degradation coefficient:
    dc = f(n)
    # print(f'degradation coefficient: {dc}')
    # generating prime numbers:
    primes = get_primes(n // dc + 1)
    # print(f'primes: {primes}')
    length = len(primes)
    # print(f'q of p: {length}')
    # pre-calculating:
    precalced_prime_sums = preprocessing(primes)
    # print(f'precalced_prime_sums: {precalced_prime_sums}')
    # print(f'q of sums: {len(precalced_prime_sums)}')
    # main algo:
    max_consecutive_length = 1
    for j in range(length):
        if j + max_consecutive_length >= length:
            # there is no need to check these primes...
            break
        consecutive_prime_sum_ = precalced_prime_sums[j + max_consecutive_length - 1] - precalced_prime_sums[j]
        for i in range(j + max_consecutive_length - 1, length):
            consecutive_prime_sum_ += primes[i]
            if consecutive_prime_sum_ >= n:
                break
            # print(f'consecutive_prime_sum_: {consecutive_prime_sum_}')
            # if this number is a prime one:
            if consecutive_prime_sum_ not in carmichael_numbers and is_prime(consecutive_prime_sum_):
                consecutive_length_ = i - j + 1
                if consecutive_length_ > max_consecutive_length:
                    max_consecutive_length = consecutive_length_
                    d[consecutive_length_] = {consecutive_prime_sum_}
                elif consecutive_length_ == max_consecutive_length:
                    d[consecutive_length_].add(consecutive_prime_sum_)
    # print(f'd: {d}')
    print(f'max_key: {max_consecutive_length}')
    return list(sorted(d[max_consecutive_length]))


def f(num: int) -> int:
    """
    theoretical optimizing function, helps to increase performance a lot by shortening the primes list...
    :param num: max number
    :return degradation coefficient:
    """
    if num < 1_000:
        return 1
    elif 1_000 <= num < 10_000:
        return 10
    elif 10_000 <= num < 100_000:
        return 25
    else:
        return 75


def preprocessing(primes: list[int]) -> list[int]:
    """
    pre-calculations...
    :param primes: consecutive prime numbers
    :return: pre-calculated consecutive prime sums
    """
    sums = [0 for _ in range(len(primes) + 1)]
    for i, prime in enumerate(primes):
        sums[i + 1] = sums[i] + prime
    return sums


def get_primes(max_num: int) -> list[int]:
    # Eratosthenes' sieve
    """
    :param max_num: max number to which we should build the primes list;
    :return: list of primes before or equal to n
    """
    # filling the list from 0 to n
    a = []
    for i in range(max_num + 1):
        a.append(i)
    # 1 is a prime number
    a[1] = 0
    # we begin from 3-rd element
    i = 2
    while i <= max_num:
        # if the cell value has not yet been nullified -> it keeps the prime number
        if a[i] != 0:
            # the first multiple will be two times larger
            j = i + i
            while j <= max_num:
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


def is_prime(x):
    return pow(2, x - 1, x) == 1


# print(f'prime or not: {is_prime(561)}')
start = time.time_ns()
longest_primes = prime_maxlength_chain(500_000)
finish = time.time_ns()
print(f'longest_primes: {longest_primes}')
print(f'time elapsed: {(finish - start) // 10 ** 6} milliseconds')
