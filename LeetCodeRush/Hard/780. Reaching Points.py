# Given four integers sx, sy, tx, and ty,
# return true if it is possible to convert the point(sx, sy) to the point(tx, ty) through some operations, or false otherwise.
import sys

# The allowed operation on some point(x, y) is to convert it to either(x, x + y) or (x + y, y).

# Example 1:
# Input: sx = 1, sy = 1, tx = 3, ty = 5
# Output: true
# Explanation: One series of moves that transforms the starting point to the target is:
# (1, 1) -> (1, 2)
# (1, 2) -> (3, 2)
# (3, 2) -> (3, 5)

# Example 2:
# Input: sx = 1, sy = 1, tx = 2, ty = 2
# Output: false

# Example 3:
# Input: sx = 1, sy = 1, tx = 1, ty = 1
# Output: true

# Constraints: 1 <= sx, sy, tx, ty <= 10 ** 9

# sys.setrecursionlimit(100_000)


def reaching_points(sx: int, sy: int, tx: int, ty: int) -> bool:
    # let us use inverse order of (tx, ty) building):
    x, y = tx, ty
    while x >= sx and y >= sy:
        print(f'{x, y = }')
        # main idea:
        if x > y:
            if y == sy and x % y == sx % y:
                return True
            x, y = x % y, y
        else:
            if x == sx and y % x == sy % x:
                return True
            x, y = x, y % x

    return False


test_case = 1, 1, 3, 5
test_case_huge = 17, 28, 11987, 28675

print(f'test case res -> {reaching_points(*test_case)}')                              # 36 366 98 989 98989 LL
print(f'test case huge res -> {reaching_points(*test_case_huge)}')
