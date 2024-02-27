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

    return rec(n, len(fibs) - 1, [])


def rec(n, i, path) -> int:
    # print(f'{n = } | {path = }')

    if n == 1:
        # print(f'{path = }')
        return 1

    result = 0

    for j in range(i, -1, -1):

        if n % fibs[j] == 0:
            result += rec(n // fibs[j], j, path + [fibs[j]])

    return result


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


super_shit = 69464323276488295902609408

start = time.time_ns()
ways = fib_prod(super_shit)
finish = time.time_ns()

print(f'{ways = }')

print(f'Time elapsed: {(finish - start) // 10 ** 6} milliseconds')


