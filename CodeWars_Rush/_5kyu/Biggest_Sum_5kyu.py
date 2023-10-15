# accepted on codewars.com
import random
import time
import sys


sys.setrecursionlimit(5_000)


def find_sum(matrix: list[list[int]]):
    memo_table = {}
    mj, mi = len(matrix), len(matrix[0])
    return path(mj - 1, mi - 1, mj, mi, matrix, memo_table)


def path(j: int, i: int, mj: int, mi: int, matrix: list[list[int]], memo_table):
    if (j, i) not in memo_table.keys():
        if not valid(j, i, mj, mi):
            memo_table[(j, i)] = 0
        else:
            memo_table[(j, i)] = max(path(j - 1, i, mj, mi, matrix, memo_table), path(j, i - 1, mj, mi, matrix, memo_table)) + matrix[j][i]
    return memo_table[(j, i)]


def valid(j: int, i: int, mj: int, mi: int):
    return 0 <= j < mj and 0 <= i < mi


m = [
    [20, 20, 10, 10],
    [10, 20, 10, 10],
    [10, 20, 20, 20],
    [10, 10, 10, 20]
]

big_m = [[random.randint(1, 1_000) for _ in range(1_000)] for _ in range(1_000)]

start = time.time_ns()
print(f'biggest sum: {find_sum(big_m)}')
finish = time.time_ns()
print(f'time elapsed str: {(finish - start) // 10 ** 6} milliseconds')

