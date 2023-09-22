# accepted on LeetCode
def max_product(nums: list[int]) -> int:
    memo_table = {}
    _, m = rec_core(len(nums) - 1, nums, memo_table)
    print(f'm: {m}')
    print(f'memo_table: {memo_table}')
    return list(sorted(memo_table.values(), key=lambda x: x[1]))[0][1]


def rec_core(i: int, nums: list[int], memo_table: dict[int, tuple[int, int]]) -> tuple[int, int]:
    if i not in memo_table.keys():
        if i == 0:
            memo_table[i] = nums[0], nums[0]
        else:
            _min, _max = rec_core(i - 1, nums, memo_table)
            if (n_ := nums[i]) > 0:
                min_, max_ = min(_min * n_, n_), max(_max * n_, n_)
            else:
                min_, max_ = min(_max * n_, n_), max(_min * n_, n_)
            memo_table[i] = min_, max_
    return memo_table[i]


arr = [1, 6, -2, 7, -4, 3, 6, 6, -1, 9]
print(f'max product subarray: {max_product(arr)}')
