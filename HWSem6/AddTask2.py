# Число 197 называется круговым простым числом, потому что все перестановки
#  его цифр с конца в начало являются простыми числами: 197, 719 и 971.
# Существует тринадцать таких простых чисел меньше 100:
# 2, 3, 5, 7, 11, 13, 17, 31, 37, 71, 73, 79 и 97.
# Сколько существует круговых простых чисел меньше миллиона?


from functools import reduce


def get_primes(n):  # Eratosthenes' sieve 36 366 98 989
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


primes_bef_1mln = get_primes(1000000)  # all primes before 1 mln
cycle_primes = list()


def cycle_check(prime: int) -> bool:  # checks if the current prime number is cycling one

    digits_list = get_digits_list(prime, [])  # creating the digits list

    for i in range(len(digits_list)):  # looking through the all different cycle-permutations of a prime number given
        temp_digit = digits_list[len(digits_list) - 1]  # the last digit
        digits_list = digits_list[:-1]  # all digits of the number except the last one
        digits_list.insert(0, temp_digit)  # new cyclically shifted number
        if reduce(lambda x, y: x * 10 + y, digits_list) not in primes_bef_1mln:  # checks if this one is located in the primes list
            return False

    cycle_primes.append(prime)

    return True


def get_digits_list(number, digits_list) -> list:  # gets the digits list of the number given
    if number == 0:
        return digits_list
    return get_digits_list(number // 10, [number % 10] + digits_list)


def count_cycle_primes():  # just an iterating through all the primes before 1 million
    count = 0

    for prime in primes_bef_1mln:
        if cycle_check(prime):
            count += 1

    return count


# print(len(get_primes(1000000)))
#
# print(get_digits_list(987, []))

print(f"cycle primes' quantity before 1 million: {count_cycle_primes()}")
print(f'cycle primes: {sorted(cycle_primes)}')

