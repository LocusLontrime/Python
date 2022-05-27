# 4. Простые делители числа 13195 - это 5, 7, 13 и 29.
# Каков самый большой делитель числа 600851475143, являющийся простым числом?

def get_primes(n):  # Eratosthenes' sieve
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


def get_max_prime_divisor(number):
    """
    :param number: a number given
    :return: max prime factor
    """
    max_prime_div = 1
    divisors = get_primes(int(number ** 0.5))  # iterating from 2 to max prime before or equal to sqrt(number)
    for i in divisors:
        if number % i == 0:
            max_prime_div = i  # the max prime factor is the last one
    return max_prime_div


print(get_primes(100))
print(get_max_prime_divisor(600851475143))
print(get_max_prime_divisor(87625999))
print(600851475143 / 6857)