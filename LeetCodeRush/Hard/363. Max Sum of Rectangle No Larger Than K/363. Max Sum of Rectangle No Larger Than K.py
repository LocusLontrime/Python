# accepted on leetcode.com

import math
from bisect import bisect_left, insort_right


def max_sum_submatrix(matrix: list[list[int]], k: int) -> int:
    # matrix's sizes:
    max_j, max_i = len(matrix), len(matrix[0])
    # 1d presums for every row:
    row_presums = [[0 for _ in range(max_i + 1)] for _ in range(max_j)]
    for j in range(max_j):
        for i in range(max_i):
            row_presums[j][i + 1] = row_presums[j][i] + matrix[j][i]
    # presums:
    for j in range(max_j):
        print(f'{j + 1} -> {row_presums[j]}')
    # now let us cycling over the every submatrix between columns i1 and i2 (0 <= i1 < i2 < max_i):
    res = -math.inf
    for i2 in range(max_i):
        for i1 in range(i2 + 1):
            # now we can find a solution for 1d case, we just need to compress row sums to integer values,
            # thus, get 1d array:
            nums = [row_presums[j][i2 + 1] - row_presums[j][i1] for j in range(max_j)]
            print(f'{i1, i2 = } | {nums = }')
            # we should increase the res variable by:
            res = max(res, max_sum_subarray(nums, k))
    # returns res:
    return res


def max_sum_subarray(nums: list[int], k: int) -> int:
    # array's length:
    n = len(nums)
    # prefix sums list:
    prefix_sums = [0]
    # the core algo:
    max_sum = -math.inf
    prefix_sum = 0
    for el in nums:
        prefix_sum += el
        print(f'{el = } | {prefix_sum = } | {prefix_sum - k = }')
        print(f'...{prefix_sums = }')
        # seeks for nearest prefix sum larger than prefix_sum - k:
        ind = bisect_left(prefix_sums, prefix_sum - k)
        print(f'...{ind = }')
        # if exists -> update max sum:
        if ind < len(prefix_sums):
            print(f'......{prefix_sum - prefix_sums[ind] = }')
            max_sum = max(max_sum, prefix_sum - prefix_sums[ind])
        # keeps prefix sums sorted:
        insort_right(prefix_sums, prefix_sum)  # if it takes O(n) -> runtime O(n ^ 4) ???
        # maybe it will be better to use SortedSet?.. but leetcode.com strictly prohibits such modules!..
    # returns res:
    return max_sum


test_ex_1d = [1, -5, 3, 6, -1, 3, 4, 6, -3], 4

test_ex = [[1, 0, 1], [0, -2, 3]], 2

print(f'test ex 1d res -> {max_sum_subarray(*test_ex_1d)}')                           # 36 366 98 989 98989
print(f'test ex res -> {max_sum_submatrix(*test_ex)}')
