# accepted on leetcode.com

import heapq


def largest_multiple_of_three(digits: list[int]) -> str:
    # digits' length:
    n = len(digits)
    rem_3 = sum(digits) % 3
    rem_eq_0_digs = [dig for dig in digits if dig % 3 == 0]
    rem_eq_1_digs = [dig for dig in digits if dig % 3 == 1]
    rem_eq_2_digs = [dig for dig in digits if dig % 3 == 2]
    heapq.heapify(rem_eq_1_digs)
    heapq.heapify(rem_eq_2_digs)
    if rem_3 == 1:
        if rem_eq_1_digs:
            heapq.heappop(rem_eq_1_digs)
        elif len(rem_eq_2_digs) > 1:
            heapq.heappop(rem_eq_2_digs)
            heapq.heappop(rem_eq_2_digs)
    elif rem_3 == 2:
        if rem_eq_2_digs:
            heapq.heappop(rem_eq_2_digs)
        elif len(rem_eq_1_digs) > 1:
            heapq.heappop(rem_eq_1_digs)
            heapq.heappop(rem_eq_1_digs)
    if len(rem_eq_1_digs) == 0 and len(rem_eq_2_digs) == 0 and set(rem_eq_0_digs) == {0}:
        rem_eq_0_digs = [0]
    return ''.join([str(dig) for dig in sorted(rem_eq_0_digs + rem_eq_1_digs + rem_eq_2_digs, reverse=True)])


test_ex = [8, 6, 7, 1, 0]
test_ex_1 = [8, 1, 9]
test_ex_2 = [1]
test_ex_err = [0, 0, 0, 1]

print(f'test ex res -> {largest_multiple_of_three(test_ex)}')                         # 36 366 98 989 98989 LL LL
print(f'test ex 1 res -> {largest_multiple_of_three(test_ex_1)}')
print(f'test ex 2 res -> {largest_multiple_of_three(test_ex_2)}')
print(f'test ex err res -> {largest_multiple_of_three(test_ex_err)}')
