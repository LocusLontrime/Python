# accepted on leetcode.com

# Given an integer array nums and an integer k, return the length of the shortest non - empty subarray of nums
# with a sum of at least k. If there is no such subarray, return -1.
import math
from collections import deque


# A subarray is a contiguous part of an array.

# Example 1:
# Input: nums = [1], k = 1
# Output: 1

# Example 2:
# Input: nums = [1, 2], k = 4
# Output: -1

# Example 3:

# Input: nums = [2, -1, 2], k = 3
# Output: 3

# Constraints:

# 1 <= nums.length <= 105
# -105 <= nums[i] <= 105
# 1 <= k <= 109

def shortest_subarray(nums: list[int], k: int) -> int:
    print(f'       {nums = }')
    # array's length:
    n = len(nums)
    # prefix sums building:
    prefix_sums = [0 for _ in range(n + 1)]
    for i, el in enumerate(nums):
        prefix_sums[i + 1] = prefix_sums[i] + el
    print(f'{prefix_sums = }')
    prefix_sum_shifted = [p + k for p in prefix_sums]
    print(f'{prefix_sum_shifted = }')
    # shortest subarray length:
    shortest_subarray_l = math.inf
    # now let us use monotonic queue:
    q = deque()
    for i in range(n):
        while len(q) > 0 and q[-1][0] > prefix_sum_shifted[i]:
            q.pop()
        q.append((prefix_sum_shifted[i], i))
        print(f'q -> {q} | {prefix_sums[i + 1]}')
        x = right_bin_search(q, prefix_sums[i + 1])
        print(f'...{x = }')
        if x >= 0:
            shortest_subarray_l = min(shortest_subarray_l, i + 1 - q[x][1])
    # returns result:
    return shortest_subarray_l


def right_bin_search(arr, goal: int):
    # array's length:
    n = len(arr)
    lb, rb = 0, n - 1
    # the core cycle:
    while lb <= rb:
        # middle index:
        mi = (lb + rb) // 2
        if arr[mi][0] <= goal:
            lb = mi + 1
        else:
            rb = mi - 1
    return lb - 1


test_ex = [2, 7, 1, 3, 6], 9
test_ex_diff = [84, -37, 32, 40, 95], 167
test_big = [-1, 84, -37, 32, -88, 9, 17, 99, -107, 22, -109, 40, 95, -19, 28, -94, 77, 89, -64, -22, -10, -109, -100, 89, -97, 90, -91, 98], 167

test_ex_1 = [-28, 81, -20, 28, -29], 89

_test =  [0, -28, 53,  33, 61,  32]
test =  [89,  61, 142, 112, 150, 111]

test_bin_search = [1, 1, 4, 6, 8, 9, 9, 9, 9, 9, 9, 9, 9, 11, 17, 18, 19, 22, 89, 98, 98989]
goal_el = 29


# print(f'monoarr test ex -> {increasing_monotonic_queue(test_ex[0])}')
# print(f'monoarr test ex diff -> {increasing_monotonic_queue(test_ex_diff[0])}')
# print(f'monoarr test ex 1 -> {increasing_monotonic_queue(test_ex_1[0])}')

#print(f'monoarr test ex -> {increasing_monotonic_queue(test)}')

# print(f'test ex res -> {shortest_subarray(*test_ex)}')                              # 36 366 98 989 98989 LL
#print(f'test ex res -> {shortest_subarray(*test_ex_diff)}')
# print(f'test ex 1 res -> {shortest_subarray(*test_ex_1)}')
print(f'test big res -> {shortest_subarray(*test_big)}')
# print(f'find ind of {11} -> {right_bin_search(test_bin_search, 11)}')
