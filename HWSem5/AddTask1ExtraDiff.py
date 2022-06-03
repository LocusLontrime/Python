# 1. Супер-сложная.
# Совершенным числом называется число, у которого сумма его делителей равна самому числу. Например,
# сумма делителей числа 28 равна 1 + 2 + 4 + 7 + 14 = 28, что означает, что число 28 является совершенным числом.
# Число n называется недостаточным, если сумма его делителей меньше n, и называется избыточным, если сумма его делителей больше n.
# Так как число 12 является наименьшим избыточным числом (1 + 2 + 3 + 4 + 6 = 16), наименьшее число, которое может быть записано
# как сумма двух избыточных чисел, равно 24. Используя математический анализ, можно показать, что все целые числа больше 28123
# могут быть записаны как сумма двух избыточных чисел. Эта граница не может быть уменьшена дальнейшим анализом, даже несмотря на то,
# что наибольшее число, которое не может быть записано как сумма двух избыточных чисел, меньше этой границы.
# Найдите сумму всех положительных чисел, которые не могут быть записаны как сумма двух избыточных чисел.

import time  # runtime evaluating 36 98 366 989


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


primes = sorted(get_primes(int(28123 ** 0.5) + 1))


def get_sum_of_factors(number):  # sum of factors excluding the number itself
    """
    :param number: number to be factorized
    :return: factorization dictionary
    """
    saved_number = number
    sum_of_factors = 1
    factor_dict = {1: 1}  # factor dictionary initialization
    for prime in primes:
        if prime * prime > number:  # get prime factors before sqrt(number)
            break
        while number != 1 and number % prime == 0:
            number //= prime
            if prime in factor_dict:
                factor_dict[prime] += 1  # increases a power (value) of this prime factor
            else:
                factor_dict[prime] = 1  # adds a new prime factor to the dict
        if number == 1:  # if a number is equal to one -> factorization is over
            break
    if number != 1:  # the last factor that is bigger than sqrt(number) is the prime factor (like in 2*3*17: 17 is the one)
        factor_dict[number] = 1

    for key, value in factor_dict.items():  # math formula for factors sum
        if key != 1:
            sum_of_factors *= (key ** (value + 1) - 1) // (key - 1)

    return sum_of_factors - saved_number  # the nuber itself should be subtracted from the factors sum


def get_non_abundant_sum():
    abundant_numbers = set()
    non_abundant_sum = 28123 * (28123 + 1) // 2  # sum of all numbers not exceeding 28123

    for num in range(1, 28123 + 1):
        if get_sum_of_factors(num) > num:  # condition of abundant number
            abundant_numbers.add(num)
        for ab_num in abundant_numbers:
            if num - ab_num in abundant_numbers:  # checking for 2-abundants representation
                non_abundant_sum -= num
                break

    return non_abundant_sum

# print(len(get_abundant_numbers()))

# print(get_sum_of_factors(12))


tic = time.perf_counter()

print(get_non_abundant_sum())

toc1 = time.perf_counter()
print(f"Time elapsed for merged sort: {toc1 - tic:0.4f} seconds")