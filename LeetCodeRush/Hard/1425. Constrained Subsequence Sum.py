# accepted on leetcode.com
from collections import deque as deq


def constrained_subset_sum(nums: list[int], k: int) -> int:
    # array's length:
    n = len(nums)
    # let us use dp:
    dp_memo = [0 for _ in range(n)]
    mono_deq = deq()
    for i in range(n):
        print(f'{i} iteration')
        if mono_deq:
            dp_memo[i] = max(0, mono_deq[-1]) + nums[i]
        else:
            dp_memo[i] = nums[i]
        if i >= k:
            if mono_deq[-1] == dp_memo[i - k]:
                mono_deq.pop()
        push_mono(mono_deq, dp_memo[i])
        print(f'{mono_deq = }')
        print(f'{dp_memo = }')
    return max(dp_memo)


def push_mono(mono_deq: deq, el: int):
    """pushing an element to decreasing monotonic deq from collections"""
    while mono_deq and mono_deq[0] < el:
        n = mono_deq.popleft()
    mono_deq.appendleft(el)


test_ex = [10, 2, -10, 5, 20], 2                                                      # 36 366 98 989 98989 LL LL
test_ex_1 = [-1, -2, -3], 1
test_ex_2 = [10, -2, -10, -5, 20], 2

print(f'test ex res -> {constrained_subset_sum(*test_ex)}')
print(f'test ex 1 res -> {constrained_subset_sum(*test_ex_1)}')
print(f'test ex 2 res -> {constrained_subset_sum(*test_ex_2)}')
