import time
import sys
from collections import defaultdict as d


sys.setrecursionlimit(100_000)


# accepted on codewars.com
def solve(arr: list[int]) -> int:
    evens = odds = sum_ = counter = 0
    for i in range(len(arr) + 1):
        sum_ += 1 if (i > 0 and arr[i - 1] % 2 != 0) else 0
        if sum_ % 2 == 0:
            counter, evens = counter + odds, evens + 1
        else:
            counter, odds = counter + evens, odds + 1
    return counter


arr_ex = [2, 3, 5, 5, 6, 8, 9, 1]  # 20
arr_example = [1, 1, 1, 1]  # 6
# [0, 1, 1, 1, 0, 0, 1, 1]
# [0, 1, 2, 3, 3, 3, 4, 5]  # 0 + 1 + 1 +
# {0: 1, 1: 1, 2: 1, 3: 3, 4: 1, 5: 1}
# [e, o, e, o, o, o, e, o], q = 0 + 1 + 1 + 2 + 2 + 2 + 4 + 3 + odds=5 = 15 + 5 = 20

# [0, 1, 2, 3, 4]

print(f'odds: {solve(arr_ex)}')




