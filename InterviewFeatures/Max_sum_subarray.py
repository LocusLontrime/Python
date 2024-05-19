import math


def max_sum_subarray(arr: list[int]) -> int:
    sum_ = 0
    max_sum = -math.inf
    _i = 0
    max_indices = (0, 0)
    for i in range(len(arr)):
        sum_ += arr[i]
        if sum_ > max_sum:
            max_sum = sum_
            max_indices = (_i, i)
        if sum_ < 0:
            sum_ = 0
            _i = i + 1

    print(f'{max_indices = }')

    return max_sum


arr_ = [-13, 4, -5, 7, 2, -1, 11, -18, 5]
arr__ = [-89, -98]

print(f'res: {max_sum_subarray(arr_)}')
print(f'res: {max_sum_subarray(arr__)}')
