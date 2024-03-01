# accepted on codewars.com
import time
from _bisect import bisect_left

MAX_N = 10_000_000
MAX_MEMO_N = sum(9 ** 2 for _ in range(len(str(MAX_N)) - 1))
SQUARES = [0, 1, 4, 9, 16, 25, 36, 49, 64, 81]

happies = []
memo_table = {0: False, 1: True, 2: False, 3: False, 4: False, 5: False, 6: False, 7: True, 8: False, 9: False}
powers_calculated = {0: 0}


# core:
def perf_happy(n: int) -> list[int]:  # 36 366 98 989 LL
    global happies

    for i in range(1, MAX_MEMO_N + 1):
        rec_happy_checker(i)

    if not happies:
        squares = {0: [0]}
        for power in range(7):
            squares_ = {}
            for i, (sq, ns) in enumerate(squares.items()):
                for d in range(10):
                    squares_.setdefault(sq + SQUARES[d], [])
                    squares_[sq + SQUARES[d]] += [n * 10 + d for n in ns]
            if power == 6:
                for k, v in squares_.items():
                    if memo_table[k]:
                        happies += v
            squares = squares_

        happies = sorted(happies)

    return happies[:bisect_left(happies, n + 1)]


# aux:
def rec_happy_checker(n: int) -> bool:
    if n not in memo_table.keys():
        memo_table[n] = rec_happy_checker(get_pow_sum(n))
    return memo_table[n]


def get_pow_sum(n: int) -> int:
    if n not in powers_calculated.keys():
        powers_calculated[n] = get_pow_sum(n // 10) + SQUARES[n % 10]
    return powers_calculated[n]


start = time.time_ns()
happy_nums = perf_happy(100)
# happy_nums_2 = perf_happy(999)
finish = time.time_ns()

print(f'Happies: {happy_nums}')
# print(f'Happies 2: {happy_nums_2}')
print(f'Size: {len(happy_nums)}')
# print(f'Size 2: {len(happy_nums_2)}')

# print(f'{memo_table = }')
# print(f'{powers_calculated = }')
print(f'All happies size: {len(happies)}')
print(f'Memo table size: {len(memo_table)}')
print(f'Memo squares size: {len(powers_calculated)}')

print(f'time elapsed: {(finish - start) // 10 ** 6} milliseconds')























# 36 366 98 989 LL
