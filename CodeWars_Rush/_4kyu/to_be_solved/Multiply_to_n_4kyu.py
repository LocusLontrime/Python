import math
from functools import reduce

from sympy.ntheory import factorint

memo_table = dict()


def multiply(n, k):

    def rec_seeker(factors, slots):  # 36 366 98 989

        if len(factors) == 0 or slots == 1:
            return 1

        memo_num = reduce(lambda x, y: x * y ** factors[y], factors.keys(), 1)

        # print(memo_num)

        if (memo_num, slots) not in memo_table.keys():

            num = len(factors) + 2

            sum_of_branches = 0

            i = 0
            for key in factors.keys():

                new_factors = factors.copy()

                if new_factors[key] == 1:
                    del new_factors[key]
                else:
                    new_factors[key] -= 1

                sum_of_branches += rec_seeker(new_factors, slots - 1)

            memo_table[(memo_num, slots)] = sum_of_branches

        return memo_table[(memo_num, slots)]

    prime_factors_dict = factorint(n)  # need to be incremented by 2 (1 and number itself)
    print(f'prime_factors_dict: {prime_factors_dict}')

    return rec_seeker(prime_factors_dict, k) // k


# print(f'res: {multiply(182, 9)}')
# print(multiply(219, 8))
print(multiply(210, 4))
# print(multiply(10, 2))
# print(multiply(36, 4))
#
# print(math.comb(10, 0))
# print(math.comb(3, 6))
# print(math.comb(12, 6))
