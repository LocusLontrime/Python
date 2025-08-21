# accepted on leetcode.com

from collections import deque as deq


def can_se_persons_count(heights: list[int]) -> list[int]:
    # array's length:
    n = len(heights)
    # queue of right heights:
    right_heights = deq()
    # the main cycle:
    res = []
    for i in range(n - 1, -1, -1):
        res += [append_el(right_heights, heights[i])]
    return res[::-1]


def append_el(rhs: deq, el: int) -> int:
    # monotonic increasing queue:
    i = 0
    while rhs and el >= rhs[0]:
        rhs.popleft()
        i += 1
    i += (1 if rhs else 0)
    rhs.appendleft(el)
    return i


test_ex = [10, 6, 8, 5, 11, 9]
test_ex_1 = [5, 1, 2, 3, 10]

print(f'test ex res -> {can_se_persons_count(test_ex)}')                              # 36 366 98 989 98989 LL LL
print(f'test ex 1 res -> {can_se_persons_count(test_ex_1)}')



