# accepted on codewars.com
import sys
from functools import lru_cache


sys.setrecursionlimit(10_000)


@lru_cache
def all_permuted(array_length):
    # base cases:
    if array_length == 1:
        return 0
    elif array_length == 2:
        return 1
    # body of rec:
    # recurrent relation:
    return (array_length - 1) * (all_permuted(array_length - 1) + all_permuted(array_length - 2))


n = 1_000
print(f'for n: {n} -->> res: {all_permuted(n)}')
