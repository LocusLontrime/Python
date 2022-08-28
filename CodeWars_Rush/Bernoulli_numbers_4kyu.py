# accepted on codewars.com (optimized with combs memoization)
import math
import time
from fractions import Fraction


def bernoulli_number(n):
    combs_saved = {(2, 0): 1, (2, 1): 2}

    def comb(n_in, k_in):
        if 2 * k_in > n_in:
            return combs_saved[(n_in, n_in - k_in)]
        else:
            if (n_in, k_in) not in combs_saved.keys():
                combs_saved[(n_in, k_in)] = comb(n_in - 1, k_in) * n_in // (n_in - k_in)
            return combs_saved[(n_in, k_in)]
    # odd bernoulli numbers are always equal to zero
    if n % 2 == 1 and n != 1:
        return 0

    memo_table = {i: Fraction(0) for i in range(0, 1500 + 1)}  # [Fraction(0, 1)] * 1500
    memo_table[0] = Fraction(1)

    for j in range(1, n + 1):
        for i in range(j):
            memo_table[j] -= comb(j + 1, i) * memo_table[i]
        memo_table[j] /= j + 1

    return memo_table[n]


t1 = time.perf_counter_ns()
print(bernoulli_number(1500))
t2 = time.perf_counter_ns()
print(f'time elapsed: {(t2 - t1) / 10 ** 6} milliseconds')
