# accepted on codewars.com
import random
from functools import reduce

MR_THRESHOLD = 5

memo_table = [0, 1, 1, 2, 4]
result_table = None
multipliers = [-1, 1, -1, 1, 1]


def k_th_last_dig_prime(k):
    if result_table is None:
        get_result_table(300 + 1)

    return result_table[k - 1]  # I don't care.


def get_result_table(max_k):
    global memo_table, result_table

    result_table = []
    seq_element = 0

    primes_found = 0
    while True:
        seq_element = reduce(lambda x, y: x + y, list(map(lambda x, y: x * y, memo_table[-5:], multipliers)), 0)
        memo_table.append(seq_element)

        if is_prime(g := get_last_9_digit_number(seq_element)):
            result_table.append([len(memo_table), g])
            primes_found += 1

        if primes_found == max_k + 1:
            break


def get_last_9_digit_number(number: int):
    if len(s := str(number)) > 8:
        return int(s[-9:])
    else:
        return 0


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
            return True
        a = pow(a, 2, p)

    return False


def is_prime(p):

    if p == 2:
        return True

    if p <= 1 or p % 2 == 0:
        return False

    return all(miller_rabin_test(random.randint(2, p - 1), p) for _ in range(MR_THRESHOLD))


# print([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11][-9:])
#
# print(get_last_9_digit_number(12345678901))

# print(k_th_last_dig_prime(1))
# print(k_th_last_dig_prime(2))
# print(k_th_last_dig_prime(3))
# print(k_th_last_dig_prime(4))
print(k_th_last_dig_prime(5))

