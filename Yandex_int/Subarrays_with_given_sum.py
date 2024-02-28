import random
import time
from collections import defaultdict


def find_subarrays(array: list[int], sum_: int):   # 36 366 98 989 LL

    good_subs = []
    prefix_sums = precalc(array)

    for prefix_sum_, indices in prefix_sums.items():
        if (r_sum := sum_ + prefix_sum_) in prefix_sums.keys():
            for lb in indices:
                for rb in prefix_sums[r_sum]:
                    if lb < rb:
                        good_subs.append(array[lb: rb])

    return good_subs


def precalc(array: list[int]) -> defaultdict[int, set[int]]:
    prefix_sums = defaultdict(set[int])
    prefix_sums[0] = {0}
    temp_key = 0

    for i, el in enumerate(array, 1):
        prefix_sums[temp_key := temp_key + el].add(i)

    return prefix_sums


sum_given = 4  # 24  #
start = time.time_ns()
arr_ = [1, 2, 4, -3, 6, -6, 7, 2, -11, 2, 3, -4, 98]  # [1, -1, 1, -1, 1, -1, 1, -1, 1, -1, 1, -1]  # [random.randint(1, 1_000_000) for _ in range(900_000)]  # [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 1]  #   # [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 1]
res = find_subarrays(arr_, sum_given)
finish = time.time_ns()

print(f'Res: {res}')
print(f'Subarrays quantity: {len(res)}')
print(f'time elapsed: {(finish - start) // 10 ** 6} milliseconds')

