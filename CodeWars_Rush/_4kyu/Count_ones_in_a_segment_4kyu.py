# accepted on codewars.com
import math


def count_ones(left, right):
    return count_ones_for_num(right) - count_ones_for_num(left - 1)


def count_ones_for_num(num: int):
    res = 0
    while num > 0:
        bin_length = int(math.log2(num))
        print(f'bin length: {bin_length}')
        res += 2 ** (bin_length - 1) * bin_length + 1 if bin_length else 1
        num -= 2 ** bin_length
        res += num
    return res


print(f'ones: {count_ones(12, 29)}')




