# accepted on codewars.com


def duplicate_or_unique(in_list: list):
    n = len(in_list)
    comparison_num1 = n * (n - 1)
    comparison_num2 = (n + 1) * (n + 3) // 4
    sum_ = sum(in_list)
    sum1, sum2 = sum_ - comparison_num1 // 2, comparison_num2 - sum_
    return sum1 if sum1 > 0 else sum2


tests = [
    [1, 2, 3, 6, 5, 4, 1],  # 1
    [1, 2, 3, 1, 2, 3, 4],  # 4
    [1, 2, 3, 6, 5, 4, 6],  # 6
    [3, 6, 9, 2, 5, 8, 1, 4, 8, 7],  # 8
[9, 8, 7, 1, 2, 3, 9, 7, 1, 2, 3, 4, 4, 5, 5, 6, 6],  # answer -> 8
]

for test in tests:
    res = duplicate_or_unique(test)
    print(f'res: {res}')
