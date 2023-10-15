# accepted on codewars.com
import math
import random
import time


def furthest_distance(arr: list[int], k: int) -> int:
    return max([abs(i - j) for j in range(len(arr)) for i in range(j + 1, len(arr)) if abs(arr[j] - arr[i]) >= k], default=-1)


def furthest_distance_(arr: list[int], k: int) -> int:
    # sorting arr's elements by value:
    sorted_indexed = sorted([(n, i) for i, n in enumerate(arr)], key=lambda x: x[0])
    # max, min precalculating:
    precalced_min_max = [(math.inf, -math.inf)] * ((length := len(arr)) + 1)
    for i in range(length - 1, -1, -1):
        _min, _max = precalced_min_max[i + 1]
        precalced_min_max[i] = min(_min, sorted_indexed[i][1]), max(_max, sorted_indexed[i][1])
    # main cycle:
    j = 0
    distance = -1
    for i in range(length):
        el, ind = sorted_indexed[i]
        while j < length and sorted_indexed[j][0] - el < k:
            j += 1
        if j != length:
            min_, max_ = precalced_min_max[j]
            distance = max(distance, abs(min_ - ind), abs(max_ - ind))
    return distance


def furthest_distance_b4b(arr, k):
    lenArr = currL = len(arr)
    while currL >= 2:
        for i in range(lenArr-currL+1):
            if abs(arr[i]-arr[currL-1+i]) >= k:
                return currL-1
        currL -= 1
    return -1


k_ = 9
arr_ = [1] * 5_000 + [98] + [1] * 5_000  # [random.randint(1, 1_000) for _ in range(10_000)]  # [11, 3, 5, 2, 3, 6, 12, 7, 98]
start = time.time_ns()
print(f'res: {furthest_distance_(arr_, k_)}')
finish = time.time_ns()
print(f'time elapsed str: {(finish - start) // 10 ** 6} milliseconds')



