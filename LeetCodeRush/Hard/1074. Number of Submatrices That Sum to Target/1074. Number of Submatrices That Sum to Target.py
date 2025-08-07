# accepted on leetcode.com

# Given a matrix and a target, return the number of non - empty submatrices that sum to target.
from collections import defaultdict


# A submatrix x1, y1, x2, y2 is the set of all cells matrix[x][y] with x1 <= x <= x2 and y1 <= y <= y2.

# Two submatrices(x1, y1, x2, y2) and (x1', y1', x2', y2') are different if they have some coordinate that is different: for example, if x1 != x1'.

# Example 1:
# Input: matrix = [[0, 1, 0], [1, 1, 1], [0, 1, 0]], target = 0
# Output: 4
# Explanation: The four 1 x1 submatrices that only contain 0.

# Example 2:
# Input: matrix = [[1, -1], [-1, 1]], target = 0
# Output: 5
# Explanation: The two 1 x2 submatrices, plus the two 2 x1 submatrices, plus the 2 x2 submatrix.

# Example 3:
# Input: matrix = [[904]], target = 0
# Output: 0

# Constraints:
# 1 <= matrix.length <= 100
# 1 <= matrix[0].length <= 100
# -1000 <= matrix[i][j] <= 1000
# -10 ^ 8 <= target <= 10 ^ 8


def num_submatrix_sum_target(matrix: list[list[int]], target: int) -> int:
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
    res = 0
    for i2 in range(max_i):
        for i1 in range(i2 + 1):
            # now we can find a solution for 1d case, we just need to compress row sums to integer values,
            # thus, get 1d array:
            nums = [row_presums[j][i2 + 1] - row_presums[j][i1] for j in range(max_j)]
            print(f'{i1, i2 = } | {nums = }')
            # we should increase the res variable by:
            res += subarray_sum(nums, target)
    # returns res:
    return res


# 560 from leetcode.com
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


test_ex = [
    [0, 1, 0],
    [1, 1, 1],
    [0, 1, 0]
], 0

print(f'test ex res -> {num_submatrix_sum_target(*test_ex)}')                         # 36 366 98 989 98989
