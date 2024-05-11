# accepted on codewars.com
import math


def triangular_sum(n: int):
    k = (-1 + math.sqrt(1 + 8 * n)) / 2
    print(f'{k = }')
    return int(math.sqrt(k)) ** 2 == k


n_ = 105  # 45
print(f'res: {triangular_sum(n_)}')



