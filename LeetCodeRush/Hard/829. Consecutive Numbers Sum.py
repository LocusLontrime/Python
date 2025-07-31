# accepted on leetcode.com

# Given an integer n, return the number of ways you can write n as the sum of consecutive
# positive integers.
import math


# Example 1:

# Input: n = 5
# Output: 2
# Explanation: 5 = 2 + 3

# Example 2:
# Input: n = 9
# Output: 3
# Explanation: 9 = 4 + 5 = 2 + 3 + 4

# Example 3:
# Input: n = 15
# Output: 4
# Explanation: 15 = 8 + 7 = 4 + 5 + 6 = 1 + 2 + 3 + 4 + 5

# Constraints: 1 <= n <= 109


def consecutive_numbers_sum(n: int) -> int:
    # integer sqrt of n:
    sqrt_2n = math.isqrt(2 * n)
    print(f'{sqrt_2n = }')
    # the main idea:
    # n could be represented as difference between i2 * (i2 + 1) and i1 * (i1 - 1) where i2 > i1, i2, i1 lies in R
    # then we compute, that for delta (between i2 and i1) = k we have:
    # 2 * i = 2 * n / (k + 1) - k, if i lies in Z+ -> we have 1 possible representation of n...
    # here comes the core cycle:
    counter = 0
    k = 0
    while 2 * n > k * (k + 1):
        if (2 * n) % (k + 1) == 0:
            val_2i = 2 * n // (k + 1) - k
            if val_2i % 2 == 0:
                counter += 1
        k += 1
        # returns res:
    return counter


m = 15
print(f'res({m}) -> {consecutive_numbers_sum(m)}')                                    # 36 366 98 989 98989 LL

print(f'{98 << 1}')
