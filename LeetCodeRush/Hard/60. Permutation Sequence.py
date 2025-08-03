# accepted on leetcode.com

import math


def get_permutation(n: int, k: int) -> str:
    k_ = k - 1
    fact_base = n - 1
    permutational_nums = [i for i in range(1, n + 1)]
    res = f''
    # result str building:
    while fact_base:
        fact = math.factorial(fact_base)
        res += f'{permutational_nums[el := k_ // fact]}'
        permutational_nums.pop(el)
        k_ = k_ % fact
        fact_base -= 1
    return res + f'{permutational_nums.pop()}'


test_ex = 4, 11
test_ex_1 = 3, 3
test_ex_2 = 4, 9
test_ex_3 = 3, 1

print(f'test ex res -> {get_permutation(*test_ex)}')
print(f'test ex 1 res -> {get_permutation(*test_ex_1)}')
print(f'test ex 2 res -> {get_permutation(*test_ex_2)}')
print(f'test ex 3 res -> {get_permutation(*test_ex_3)}')


