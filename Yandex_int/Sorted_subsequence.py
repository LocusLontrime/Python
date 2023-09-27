# The Task: Count all sorted subsequences:
import random
import time
import operator


# O(exp(n)) -->> can break every PC easily...
def i_am_brut(arr: list[int]):
    # how to use brut here?
    # do not want to use rec...
    ...


def common_sequences(arr: list[int], non_decr: bool = True):
    """counts all the common subsequences of the array given, so that subsequences that are not (non)increasing or (non)decreasing..."""
    return 2 ** len(arr) - 1 - sorted_subsequences(arr, non_decr=True) - sorted_subsequences(arr, non_decr=False) + len(arr)  # doubly-subtracted subsequences with the length of 1


# O(n^2) -->> dynamic programming...
def sorted_subsequences(arr: list[int], non_decr: bool = True):
    memo_table = {}
    for i, el in enumerate(arr):
        if i not in memo_table.keys():
            rec_core(i, arr, memo_table, non_decr)
    print(f'memo_table: {memo_table}')
    return sum(memo_table.values())


def rec_core(i: int, arr: list[int], memo_table: dict[int, int], non_decr: bool):
    if i not in memo_table.keys():
        # border case:
        counter = 1  # the element itself as valid subsequence:
        bin_op = operator.le if non_decr else operator.ge
        # cycling all left subs:
        if i != 0:
            for ind in range(i):
                if bin_op(arr[ind], arr[i]):
                    counter += rec_core(ind, arr, memo_table, non_decr)
        # write counter to memo table:
        memo_table[i] = counter
    # returning interim result:
    return memo_table[i]


arr_ = [1, 2, 1, 3, 4, 5, 2]

arr_big = [random.randint(1, 1_000_000) for _ in range(1_000)]

start1 = time.time_ns()
print(f'i_am_brut: {i_am_brut(arr_big)}')
start2 = time.time_ns()
print(f'sorted_subsequences: {sorted_subsequences(arr_big)}')
start3 = time.time_ns()
print(f'common_subsequences: {common_sequences(arr_big)}')
start4 = time.time_ns()


print(f'time elapsed brut: {(start2 - start1) // 10 ** 6} milliseconds')
print(f'time elapsed dp: {(start3 - start2) // 10 ** 6} milliseconds')
print(f'time elapsed: common_sequences: {(start4 - start3) // 10 ** 6} milliseconds')
















































