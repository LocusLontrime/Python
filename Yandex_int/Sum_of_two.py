import math


def closest_sum(array: list[int], element: int) -> tuple[int, int]:
    lp, rp = 0, len(array) - 1
    bfp: tuple[int, int]
    min_delta = math.inf
    # two-pointers strategy:
    while lp < rp:
        current_sum = array[lp] + array[rp]
        if current_sum == element:
            return lp, rp
        else:
            if (d_ := abs(element - current_sum)) < min_delta:
                min_delta = d_
                bfp = lp, rp
            if current_sum < element:
                lp += 1
            else:
                # current_sum > element:
                rp -= 1
    return bfp


array_ = [1, 3, 6, 6, 6, 17, 22, 23, 76, 89, 98, 99, 989, 999, 98989]
element_ = 12

print(f'bfp: {closest_sum(array_, element_)}')

