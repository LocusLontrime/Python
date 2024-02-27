# accepted on codewars.com
import time

MAX_FIB = 10 ** 36 + 1
fibs = {}

memo_table = {}


def fib_prod(n: int) -> int:
    x, y = 1, 2

    if not fibs:

        i = -1
        while x < MAX_FIB:
            x, y = y, y + x
            fibs[i := i + 1] = x

    print(f'{n = }')  # | {fibs = }

    ways, paths = rec(n, len(fibs) - 1)

    print(f'PATHS: ')

    for i, path in enumerate(paths[::-1], 1):
        print(f'{i}th {path = }')

    return ways  # rec_(n, len(fibs) - 1)


# for visual purpose only!
def rec(n, i) -> tuple[int, list[list[int]]]:

    if n == 1:
        return 1, [[]]

    if (n, i) not in memo_table.keys():

        memo_table[(n, i)] = [0, []]

        for j in range(i, -1, -1):

            if n % fibs[j] == 0:
                q, paths = rec(n // fibs[j], j)
                memo_table[(n, i)][0] += q
                memo_table[(n, i)][1] += [path + [fibs[j]] for path in paths]

    return memo_table[(n, i)]


# faster!!!
def rec_(n, i) -> int:

    if n == 1:
        return 1

    if (n, i) not in memo_table.keys():

        memo_table[(n, i)] = 0
        for j in range(i, -1, -1):
            if n % fibs[j] == 0:
                memo_table[(n, i)] += rec_(n // fibs[j], j)

    return memo_table[(n, i)]


super_shit = 62036862929638945581957120000000000000000000000000000000 * 2 ** 16 * 5 ** 5 * 8 ** 4 * 89 ** 3

start = time.time_ns()
ways_ = fib_prod(super_shit)
finish = time.time_ns()

print(f'{ways_ = }')

print(f'Time elapsed: {(finish - start) // 10 ** 6} milliseconds')


