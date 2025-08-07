# accepted on leetcode.com
# Given an integer array nums and two integers lower and upper, return the number of range sums that lie in [lower, upper] inclusive.
import math
from sortedcontainers import SortedList
# Range sum S(i, j) is defined as the sum of the elements in nums between indices i and j inclusive, where i <= j.

# Example 1:
# Input: nums = [-2, 5, -1], lower = -2, upper = 2
# Output: 3
# Explanation: The three ranges are: [0, 0], [2, 2], and [0, 2] and their respective sums are: -2, -1, 2.

# Example 2:
# Input: nums = [0], lower = 0, upper = 0
# Output: 1

# Constraints:
# 1 <= nums.length <= 10 ** 5
# -231 <= nums[i] <= 231 - 1
# -105 <= lower <= upper <= 105
# The answer is guaranteed to fit in a 32 - bit integer.


def count_range_sum(nums: list[int], lower: int, upper: int) -> int:
    # array's length:
    n = len(nums)
    # prefix sums:
    presums = SortedList([-math.inf, 0, math.inf])  # borders for convenience
    presum = 0
    # core algo:
    res = 0
    for i in range(n):
        presum += nums[i]
        res += presums.bisect_right(presum - lower) - presums.bisect_left(presum - upper)  # ri - li
        presums.add(presum)
    return res


test_ex = [-2, 5, -1], -2, 2

test_ex_1 = [0], 0, 0
test_ex_2 = [0, 0], 0, 0
test_ex_3 = [-1, 1], 0, 0
test_ex_4 = [2147483647, -2147483648, -1, 0], -1, 0

print(f'test ex res -> {count_range_sum(*test_ex)}')                                  # 36 366 98 989 98989 LL
print(f'test ex 1 res -> {count_range_sum(*test_ex_1)}')
print(f'test ex 2 res -> {count_range_sum(*test_ex_2)}')
print(f'test ex 3 res -> {count_range_sum(*test_ex_3)}')
print(f'test ex 4 res -> {count_range_sum(*test_ex_4)}')
