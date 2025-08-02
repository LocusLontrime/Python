# Given an integer n, return an array ans of length n + 1 such that for each i(0 <= i <= n),
# ans[i] is the number of 1's in the binary representation of i.
import math

# Example 1:
# Input: n = 2
# Output: [0, 1, 1]
# Explanation:
# 0 --> 0
# 1 --> 1
# 2 --> 10

# Example 2:
# Input: n = 5
# Output: [0, 1, 1, 2, 1, 2]
# Explanation:
# 0 --> 0
# 1 --> 1
# 2 --> 10
# 3 --> 11
# 4 --> 100
# 5 --> 101


# Constraints: 0 <= n <= 10 ** 5


MAX_N = 10 ** 5
ones_q = []


def count_bits(n: int) -> list[int]:
    global ones_q
    # let us precompute a bit:
    if not ones_q:
        max_power_of_2 = int(math.log2(MAX_N)) + 1
        ones_q = [0] * 2 ** max_power_of_2
        ones_q[1] = 1
        print(f'{max_power_of_2 = }')
        for power_of_2 in range(1, max_power_of_2):
            powered_2 = 2 ** power_of_2
            for i in range(powered_2, 2 * powered_2):
                ones_q[i] = 1 + ones_q[i - powered_2]
        print(f'{ones_q = }')
    return ones_q[:n + 1]


# arr = [1, 5, 4, 8, 98, 9, 2, 989]

test_ex = 5

print(f'res -> {count_bits(test_ex)}')
