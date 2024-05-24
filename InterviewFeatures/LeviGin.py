import math


def max_sum_subarray(arr: list[int]) -> list[int]:
    sum_ = 0
    max_sum = -math.inf
    bli, bri = (0, 0)
    li_ = 0

    for i, el in enumerate(arr):
        sum_ += el

        print(f'{i = } | {sum_ = }')

        if sum_ >= 0:
            if sum_ > max_sum:
                max_sum = sum_
                bli, bri = li_, i
        else:
            sum_ = 0
            li_ = i + 1

    return arr[bli: bri + 1]


array = [1, 7, -1, -8, 9, 19, -17, 98, -9, -100, 18, 81, -117, 98]
array_x = [-98]

print(f'res: {max_sum_subarray(array_x)}')

# print(f'res: {vars(object)}')
