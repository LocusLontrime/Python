# accepted on leetcode.com
import math


def largest_number(cost: list[int], target: int) -> str:
    # array's length:
    n = len(cost)
    # let us use dp:
    memo_table = {}
    prevs = {}
    max_l = dp(target, cost, memo_table, prevs)
    print(f'{max_l = }')
    print(f'{memo_table = }')
    print(f'{prevs = }')
    if max_l < 0:
        return "0"
    t = target, 0
    max_num = f''
    while prevs[t[0]] is not None:
        t = prevs[t[0]]
        max_num += f'{t[1]}'
    return max_num


def dp(target: int, cost: list[int], memo_table: dict, prevs: dict) -> int:
    # border case:
    if target == 0:
        prevs[0] = None
        return 0
    # body of rec:
    if target not in memo_table.keys():
        res = -math.inf
        for digit in range(1, 10):
            target_ = target - cost[digit - 1]
            if target_ >= 0:
                r = dp(target_, cost, memo_table, prevs) + 1
                if r >= 0 and r >= res:
                    res = r
                    prevs[target] = target_, digit
        memo_table[target] = res
    return memo_table[target]


test_ex = [4, 3, 2, 5, 6, 7, 2, 5, 5], 9
test_ex_1 = [7, 6, 5, 5, 5, 6, 8, 7, 8], 12
test_ex_2 = [2, 4, 6, 2, 4, 6, 4, 4, 4], 5

print(f'test ex res -> {largest_number(*test_ex)}')                                   # 36 366 98 989 98989 LL LL
print(f'test ex 1 res -> {largest_number(*test_ex_1)}')
print(f'test ex 2 res -> {largest_number(*test_ex_2)}')


