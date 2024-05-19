def max_sum_subsequence(arr: list[int]) -> int:
    return sum(n for n in arr if n > 0)


arr_ = [1, -7, 8, 6, -11, 6, 2, 0, -98, 7, 98]

print(f'res: {max_sum_subsequence(arr_)}')
