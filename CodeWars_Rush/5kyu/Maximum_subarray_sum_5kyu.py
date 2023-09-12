# accepted on codewars.com
import sys
max_res: int


sys.setrecursionlimit(50_000)


def max_sequence(arr: list[int]):
    global max_res
    max_res = 0
    dp(len(arr) - 1, arr)
    return max_res


def dp(i: int, arr: list[int]) -> int:
    global max_res
    res = arr[i] if i == 0 else max(dp(i - 1, arr) + arr[i], arr[i])
    max_res = max(max_res, res)
    return res


array = [-2, 1, -3, 4, -1, 2, 1, -5, 4]
print(f'res: {max_sequence(array)}')
# should be 6: [4, -1, 2, 1]


