# accepted on leetcode.com

# There are several squares being dropped onto the X - axis of a 2D plane.

# You are given a 2D integer array positions where positions[i] = [left_i, sideLength_i] represents the i_th square
# with a side length of sideLength_i that is dropped with its left edge aligned with X-coordinate left_i.

# Each square is dropped one at a time from a height above any landed squares.
# It then falls downward(negative Y direction) until it either lands on the top side of another square or on the X - axis.
# A square brushing the left / right side of another square does not count as landing on it.
# Once it lands, it freezes in place and cannot be moved.

# After each square is dropped, you must record the height of the current tallest stackof squares.

# Return an integer array ans where ans[i] represents the height described above after dropping the ith square.

# Example 1:
# Input: positions = [[1, 2], [2, 3], [6, 1]]
# Output: [2, 5, 5]
# Explanation: After the first drop, the tallest stack is square 1 with a height of 2.
# After the second drop, the tallest stack is squares 1 and 2 with a height of 5.
# After the third drop, the tallest stack is still squares 1 and 2 with a height of 5.
# Thus, we return an answer of [2, 5, 5].

# Example 2:
# Input: positions = [[100, 100], [200, 100]]
# Output: [100, 100]
# Explanation: After the first drop, the tallest stack is square 1 with a height of 100.
# After the second drop, the tallest stack is either square 1 or square 2, both with heights of 100.
# Thus, we return an answer of [100, 100].
# Note that square 2 only brushes the right side of square 1, which does not count as landing on it.

# Constraints:
# 1 <= positions.length <= 1000
# 1 <= lefti <= 10 ** 8
# 1 <= sideLengthi <= 10 ** 6

# O(n^2) with coords' compressing (should be optimized by using a max segment tree with lazy propagation)
def falling_squares(positions: list[list[int]]) -> list[int]:
    # 1. coordinates compressing:
    coords = set()
    for li, side in positions:
        coords |= {li, li + side - 1}
    compress = {el: i for i, el in enumerate(sorted(coords))}
    n = len(compress)
    # 2. the main part of finding the max heights at the every square's falling:
    heights = [0 for _ in range(n)]
    max_height = 0
    ans = []
    for li, side in positions:
        max_h_under = max(heights[compress[li]: compress[li + side - 1] + 1])
        for i in range(compress[li], compress[li + side - 1] + 1):
            heights[i] = max_h_under + side
        max_height = max(max_height, max_h_under + side)
        ans += [max_height]
    return ans


test_ex = [
    [1, 2],
    [2, 3],
    [6, 1]
]

test_ex_1 = [
    [100, 100],
    [200, 100]
]

print(f'test ex res -> {falling_squares(test_ex)}')                                   # 36 366 98 989 98989 LL
print(f'test ex 1 res -> {falling_squares(test_ex_1)}')
