# The Task: Count all the nice subarrays of the array given.
# Subarray is nice if
# 1. length is greater than 1;
# 2. leftmost element is less or equals than sum(arr)
# 3. rightmost element is greater or equals than sum(arr)

# Notes:
# all estimations based on the worst case...
# 1. Bruteforce -->> runtime: O(n^3), additional memory: O(n)
# 2. Accurate BruteForce -->> runtime: O(n^2), additional memory: O(1)
# 3. Divide and Conquer -->> runtime: O(n * log(n)), additional memory: O(n)


import random
import time


# O(n^3)
def i_am_brut(arr: list[int]):  # 36 366 98 989 LL
    counter = 0
    for j in range(len(arr)):
        for i in range(j + 1, len(arr)):
            if arr[j] <= sum(arr[j: i + 1]) / (i + 1 - j) <= arr[i]:
                counter += 1
    return counter


# O(n^2)
def i_am_accurate_brut(arr: list[int]):
    counter = 0
    for j in range(len(arr)):
        sum_ = arr[j]
        for i in range(j + 1, len(arr)):
            sum_ += arr[i]
            if arr[j] <= sum_ / (i + 1 - j) <= arr[i]:
                counter += 1
    return counter


arr_ = [1, 5, 7, 3, 2, 6, 2, 2, 2, 1, 5, 9]
arr_big = [random.randint(-100, 100) for _ in range(1_000)]

start1 = time.time_ns()
print(f'i_am_brut: {i_am_brut(arr_big)}')
start2 = time.time_ns()
print(f'i_am_accurate_brut: {i_am_accurate_brut(arr_big)}')
start3 = time.time_ns()

print(f'time elapsed brut: {(start2 - start1) // 10 ** 6} milliseconds')
print(f'time elapsed accurate brut: {(start3 - start2) // 10 ** 6} milliseconds')


