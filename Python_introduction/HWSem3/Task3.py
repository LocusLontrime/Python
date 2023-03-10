# Составить список простых множителей натурального числа N
import math
import time


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


def get_factors(number: int):
    primes = get_primes(int(math.sqrt(number)))
    factorization_dictionary = {}
    for prime in primes:
        power_counter = 0
        while number % prime == 0:
            number //= prime
            power_counter += 1
        if power_counter >= 1:
            factorization_dictionary[prime] = power_counter
    if number > 1:
        factorization_dictionary[number] = 1
    return factorization_dictionary


# METHOD: PRIME FACTORS, from stackoverflow.com:
def get_prime_factors(n):
    num = n
    count = 0
    index = 0
    factors_candidates = [2, 3, 5, 7]
    factors = []
    while factors_candidates[index] ** 2 <= n:
        count += 1
        if len(factors_candidates) == (index + 1):
            factors_candidates.append(factors_candidates[-2] + 6)
        if n % factors_candidates[index]:
            index += 1
        else:
            n = n // factors_candidates[index]
            factors.append(factors_candidates[index])
    if n > 1:
        factors.append(n)
    print(f't: {factors_candidates}')
    return num, factors, f'count optimization: {count}'


k = 3*3*3*3*3*11*17*199*10017
# print(get_factors(640320))
# print(get_factors(6670))
# print(get_factors(640320 // (32 * 3)))
# print(get_factors(13717421))
# print(get_factors(36758392918475747))
start = time.time_ns()
print(f'k: {k}')
# print(get_factors(k))
print(get_prime_factors(k))
finish = time.time_ns()
print(f'time elapsed: {(finish - start) // 10 ** 6} milliseconds')

# l = list(sorted(get_primes(20000)))
#
# print(f'length: {len(l)}, l: {l}')

