# The Task: Count all sorted subsequences:
import random
import time


# O(exp(n)) -->> can break every PC easily...
def i_am_brut(arr: list[int]):
    # how to use brut here?
    # do not want to use rec...
    ...


# O(n^2) -->> dynamic programming...
def sorted_subsequences(arr: list[int]):
    memo_table = {}
    for i, el in enumerate(arr):
        if i not in memo_table.keys():
            rec_core(i, arr, memo_table)
    print(f'memo_table: {memo_table}')
    return sum(memo_table.values())


def rec_core(i: int, arr: list[int], memo_table: dict[int, int]):
    if i not in memo_table.keys():
        # border case:
        if i == 0:
            return 1
        # cycling all left subs:
        counter = 1  # the element itself as valid subsequence:
        for ind in range(i):
            if arr[ind] <= arr[i]:
                counter += rec_core(ind, arr, memo_table)
        # write counter to memo table:
        memo_table[i] = counter
    # returning interim result:
    return memo_table[i]


arr_ = [1, 2, 1, 3, 4, 5, 2]

arr_big = [random.randint(1, 100) for _ in range(100)]

start1 = time.time_ns()
print(f'i_am_brut: {i_am_brut(arr_big)}')
start2 = time.time_ns()
print(f'sorted_subarrays: {sorted_subsequences(arr_big)}')
start3 = time.time_ns()

print(f'time elapsed brut: {(start2 - start1) // 10 ** 6} milliseconds')
print(f'time elapsed dp: {(start3 - start2) // 10 ** 6} milliseconds')
















































