# n992 from leetcode.com
# accepted on leetcode.com
from collections import defaultdict as d


def subs_k_distincts(nums: list[int], k: int) -> int:
    occurrences: d[int, int] = d(int)
    counter, current_distincts_q = 0, 0
    li, ri, start, end = 0, 0, 0, 0
    # the core cycle (sliding window):
    while li < len(nums):  # i -> (start_i, end_i): counter += end_i - start_i
        # start border defining:
        while ri < len(nums) and current_distincts_q < k:
            if not occurrences[nums[ri]]:
                current_distincts_q += 1
            occurrences[nums[ri]] += 1
            ri += 1
        start = ri
        ri = max(ri, end)
        # end border defining:
        while ri < len(nums) and current_distincts_q == k:
            if not occurrences[nums[ri]]:
                break
            ri += 1
        end = ri
        # counter increasing:
        if current_distincts_q == k:
            counter += ri - start + 1
        # li step forward:
        occurrences[nums[li]] -= 1
        if occurrences[nums[li]] == 0:
            current_distincts_q -= 1
        # next step preparations:
        li += 1
        ri = start
    return counter


nums_ = [48, 18, 15, 17, 35, 33, 3, 22, 14, 52, 18, 32, 45, 33, 39, 7, 52, 2, 4, 22, 13, 41, 4, 29, 3, 7, 34, 31, 4, 49,
         3, 8, 20, 42, 12, 11, 35, 42, 3, 21, 27, 29, 37, 21, 40, 50, 22, 7, 2, 32, 1, 1, 22, 33, 19, 52, 38, 34, 36,
         48, 40, 28, 47, 8, 7, 46, 17, 7, 2, 21, 49, 6, 7, 50, 15, 31, 50, 52, 1, 27, 3, 15, 5, 6, 23, 26, 34, 50, 15,
         22, 26, 39, 28, 25, 25, 21, 37, 28, 45]  # [2, 2, 1, 2, 2, 2, 1, 1]  # [1, 2, 1, 2, 3]  # [1, 2, 1, 3, 4]
nums_x = [1, 2, 3, 3, 3, 2, 1]
k_ = 30  # 2, 3
k_x = 3

print(f'res: {subs_k_distincts(nums_x, k_x)}')                                 # 98
