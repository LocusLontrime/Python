# accepted on codewars.com
from functools import reduce


def greatest_product(st: str) -> int:
    nums, len_ = list(map(int, st)), len(st)
    return max(reduce(lambda x, y: x * y, nums[i: i + 5]) for i in range(0, len_ - 5 + 1))      # 36 366 98 989 98989 LL 


print(f'res -> {greatest_product("92494737828244222221111111532909999")}')
