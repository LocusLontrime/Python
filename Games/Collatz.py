import math
import sys
import time

sys.setrecursionlimit(100_000)

memo_table = {}


def collatzify(n: int) -> int:
    steps = 0

    # print(f'n: {n}')
    # print(f"Collatz's calculus started: \n")

    while n - 1:
        steps += 1
        if steps > 10e6:
            raise ValueError(f'Collatz mistaken!')
        _n = n
        if n % 2:
            # print(f'{n} -> 3*{n} + 1 = {3*n + 1}')
            n = 3 * n + 1
        else:
            # print(f'{n} -> {n} // 2 = {n // 2}')
            n //= 2

    return steps


def rec_collatzify(n: int) -> int:
    # 1. border cases:
    if n == 1:
        return 0

    # 2. body of recursion:
    if n in memo_table.keys():
        return memo_table[n]

    # 3. recurrent relation:
    memo_table[n] = rec_collatzify(3 * n + 1 if n % 2 else n // 2) + 1
    return memo_table[n]


def get_collatz_results(n: int):
    res, iters = collatzify(n)
    print(f"\nResult of Collatz's calculus: {res}, "
          f"this process done in {iters} iterations")


# start_ = time.time_ns()
# max_steps = 0
# max_steps_i = ...
# for i in range(1, 1_000_000 + 1):
#     curr_steps = rec_collatzify(i)
#     if curr_steps > max_steps:
#         max_steps = curr_steps
#         max_steps_i = i
# finish_ = time.time_ns()
#
# print(f'{max_steps_i, max_steps = }')
# print(f'Time elapsed: {(finish_ - start_) // 10 ** 6} ms')

# steps_3 = rec_collatzify(3)
# steps_6 = rec_collatzify(6)

# print(f'{steps_3, steps_6 = }')

# print(f'{memo_table = }')

steps_ = collatzify(num_ := 1_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_001)
print(f'{steps_ = }')
print(f'{math.log2(num_)}')