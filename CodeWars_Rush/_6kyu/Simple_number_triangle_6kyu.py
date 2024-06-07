# accepted on codewars.com
import time
import sys


sys.setrecursionlimit(1_000)


# CATALANs NUMBERS... can be done in O(1)...)
def solve(n):
    memo_table = {(j, 0): 1 for j in range(n + 1)}
    res = simple_triangle_num(n, n, memo_table)

    # for j in range(n + 1):
    #     for i in range(j):
    #         print(f'{memo_table[j, i]} ', end='')
    #     print()
    return res                                                                        # 36 366 98 989 98989 LL


def simple_triangle_num(j: int, i: int, memo_table: dict) -> int:
    # print(f'{j, i = }')

    # base cases:
    if i > j:
        return 0
    # core:
    if (j, i) not in memo_table.keys():
        memo_table[(j, i)] = simple_triangle_num(j, i - 1, memo_table) + simple_triangle_num(j - 1, i, memo_table)

    return memo_table[(j, i)]


k = 200

start = time.time_ns()
print(f'res({k}) -> {solve(k)}')  # 1430
finish = time.time_ns()

print(f'time elapsed: {(finish - start) // 10 ** 6} milliseconds')

