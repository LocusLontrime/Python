# -*- coding: utf-8 -*-
# Определить Наибольшую Возрастающую Последовательность в массиве целых чисел


# O(n^2 -> dp)
def lis(array: list[int]):
    # array's length:
    n = len(array)
    # memoization:
    memo_table = [0 for _ in range(n)]  # lengths of longest subsequences with the last element in the index i
    index_chain = [0 for _ in range(n)]  # for restoring the LIS!
    # recursive start:
    for j in range(n):
        rec_core(j, array, memo_table, index_chain)
    # memo tables:
    print(f'{memo_table = }')
    print(f'{index_chain = }')
    # lis restoring:
    j, max_lis_length = max([(_, l) for _, l in enumerate(memo_table)], key=lambda x: x[1])
    print(f'{j, max_lis_length = }')
    lis_str = f''
    while j != -1:
        lis_str = f'{array[j]}|{lis_str}'
        j = index_chain[j]
    return max(memo_table), f'|{lis_str}'


def rec_core(i: int, array: list[int], memo_table: list[int], index_chain: list[int]):
    # body of recursion:
    if not memo_table[i]:
        res = 1
        index_chain[i] = -1
        for k in range(i):
            # recurrent relation:
            if array[i] > array[k]:
                if (r := max(res, rec_core(k, array, memo_table, index_chain) + 1)) > res:
                    res = r
                    index_chain[i] = k
        memo_table[i] = res
    return memo_table[i]


test_ex = [5, 10, 6, 12, 3, 24, 7, 8, 1, 7, 1, 98, 89, 99, 12, 18, 98, 1, 8, 99, 2, 88]

print(f'res -> {lis(test_ex)}')                                                       # 36 366 98 989 98989 LL
