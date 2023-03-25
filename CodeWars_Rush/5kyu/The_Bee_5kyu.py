# accepted on codewars (bottom-up only)
import sys
import time

sys.setrecursionlimit(1000000)


# covering:
def the_bee(n: int):
    """top-down version, too slow"""
    ...
    "Good luck, ebi sobak!"
    # memoization:
    dp = dict()
    # restrictions:
    k = n - 1
    length = 2 * k + 1

    restricted_cells = set()
    for j in range(n - 1):
        for i in range(j, n - 1):
            restricted_cells.add((j, n + i))
            restricted_cells.add((n + i, j))

    # core function:
    def rec_path_seeker(y: int, x: int):
        if (y, x) not in restricted_cells:
            # base case:
            if length - 1 in [y, x]:
                return 1
            # recursion body:

            # memo check:
            if (y, x) not in dp.keys():
                # recurrent relation:
                y_, x_ = y + 1, x + 1
                dp[(y, x)] = rec_path_seeker(y_, x) + rec_path_seeker(y, x_) + rec_path_seeker(y_, x_)
            return dp[(y, x)]
        else:
            return 0

    return rec_path_seeker(0, 0)


def the_bee_(n: int):
    """bottom-up version"""
    length = 2 * n - 1
    print(f'length: {length}')
    # memoization:
    dp = [[0] * length for _ in range(length)]
    # restrictions:
    restricted_cells = set()
    for j in range(n - 1):
        for i in range(j, n - 1):
            restricted_cells.add((j, n + i))
            restricted_cells.add((n + i, j))
    # main cycle:
    for j in range(length):
        for i in range(length):
            if (j, i) not in restricted_cells:
                # base case:
                if 0 in [j, i]:
                    # print(f'zero for: {j=}, {i=}')
                    dp[j][i] = 1
                else:
                    # print(f'try to calc: {j=}, {i=}')
                    dp[j][i] = dp[j - 1][i] + dp[j][i - 1] + dp[j - 1][i - 1]
            else:
                dp[j][i] = 0
    return dp[length - 1][length - 1]


# covering:
def robot(y_max: int, x_max: int):
    # memoization:
    dp = dict()

    # core function:
    def rec_path_seeker(y: int, x: int):
        # base case:
        if y == y_max - 1 or x == x_max - 1:
            return 1
        # recursion body:

        # memo check:
        if (y, x) not in dp.keys():
            # recurrent relation:
            dp[(y, x)] = rec_path_seeker(y + 1, x) + rec_path_seeker(y, x + 1)
        return dp[(y, x)]

    return rec_path_seeker(0, 0)


start = time.time_ns()
# print(f'ways: {robot(1117, 1115)}')
# print(f'bee ways 3: {the_bee(200)}')
print(f'bee_ ways 3: {the_bee_(200)}')
# print(f'bee ways 2: {the_bee(2)}')
finish = time.time_ns()

print(f'time elapsed: {(finish - start) // 10 ** 6} milliseconds')


