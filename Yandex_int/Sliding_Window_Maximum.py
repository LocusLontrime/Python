from collections import deque as deq


def max_sliding_window(nums: list[int], k: int) -> list[int]:
    mono_deq = deq()
    # sliding window fulfilling:
    for i in range(k):
        push_mono(mono_deq, nums[i])
    yield mono_deq[-1]
    for i in range(k, len(nums)):
        if nums[i - k] == mono_deq[-1]:
            mono_deq.pop()
        push_mono(mono_deq, nums[i])
        yield mono_deq[-1]
    print(f'mono_deq: {mono_deq}')


def push_mono(mono_deq: deq, el: int):
    """pushing element to decreasing monotonic deq"""
    while mono_deq and mono_deq[0] < el:
        mono_deq.popleft()
    mono_deq.appendleft(el)


nums_, k_ = [1, 4, 9, 3, 2, 6, 8, 7, 6, 1, 5, 9], 5
nums_ex, k_ex = [1, 3, -1, -3, 5, 3, 6, 7], 3
nums_ex_, k_ex_ = [9, 8, 7, 6, 5, 4, 3, 2, 1], 3

print(f'res: {list(max_sliding_window(nums_ex, k_ex))}')
