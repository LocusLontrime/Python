# accepted on codewars.com
import time


def climbing_stairs(costs: list[int]):
    memo_table = {}
    return dp(len(costs), costs + [0], memo_table)


def dp(i: int, costs: list[int], memo_table: dict[int, int]) -> int:
    if i not in memo_table.keys():
        # border case:
        if i in [0, 1]:
            return costs[i]
        # recurrent relation:
        memo_table[i] = min(dp(i - 1, costs, memo_table), dp(i - 2, costs, memo_table)) + costs[i]
    return memo_table[i]


arr = [0, 2, 3, 2, 0]
start = time.time_ns()
print(f'min cost: {climbing_stairs(arr)}')
finish = time.time_ns()
print(f'time elapsed: {(finish - start) // 10 ** 6} milliseconds')
