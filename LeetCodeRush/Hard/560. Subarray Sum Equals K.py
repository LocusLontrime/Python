# accepted on leetcode.com

# Given an array of integers nums and an integer k, return the total number of subarrays whose sum equals to k.

# A subarray is a contiguous non - empty sequence of elements within an array.

# Example 1:
# Input: nums = [1, 1, 1], k = 2
# Output: 2

# Example 2:
# Input: nums = [1, 2, 3], k = 3
# Output: 2

# Constraints:
# 1 <= nums.length <= 2 * 104
# -1000 <= nums[i] <= 1000
# -107 <= k <= 107

from collections import defaultdict


def subarray_sum(nums: list[int], k: int) -> int:
    # array's length:
    n = len(nums)
    # prefix sums frequencies:
    pref_sums_freqs = defaultdict(int)
    pref_sums_freqs[0] = 1
    # the core algo:
    res = 0
    pref_sum_ = 0
    for el in nums:
        # new prefix sum:
        pref_sum_ += el
        # check for the target sum:
        res += pref_sums_freqs[pref_sum_ - k]
        # pref_sums_freqs updating:
        pref_sums_freqs[pref_sum_] += 1
    # returns res:
    return res


test_ex = [1, 1, 1], 2

test_ex_1 = [1, 2, 3], 3

print(f'test ex res -> {subarray_sum(*test_ex)}')                                     # 36 366 98 989 98989
print(f'test ex 1 res -> {subarray_sum(*test_ex_1)}')
