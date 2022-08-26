# accepted on codewars.com
import math
from fractions import Fraction


def bernoulli_number(n):
    # odd bernoulli numbers are always equal to zero
    if n % 2 == 1 and n != 1:
        return 0

    memo_table = {i: Fraction(0) for i in range(0, 1500 + 1)}  # [Fraction(0, 1)] * 1500
    memo_table[0] = Fraction(1)

    for j in range(1, n + 1):
        for i in range(j):
            memo_table[j] -= math.comb(j + 1, i) * memo_table[i]
        memo_table[j] /= j + 1

    return memo_table[n]


# print(math.comb(5, 3))
# print(Fraction(2, 3))
# print({i: 0 for i in range(0, 1500 + 1)})

# print(Fraction(1, 2) * 3)

print(bernoulli_number(500))

