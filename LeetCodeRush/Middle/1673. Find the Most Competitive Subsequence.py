# accepted on leetcode.com
from collections import deque


# Given an integer array nums and a positive integer k, return the most competitive subsequence of nums of size k.

# An array's subsequence is a resulting sequence obtained by erasing some (possibly zero) elements from the array.

# We define that a subsequence a is more competitive than a subsequence b(of the same length)
# if in the first position where a and b differ, subsequence a has a number less than the corresponding number in b.
# For example, [1, 3, 4] is more competitive than[1, 3, 5]
# because the first position they differ is at the final number, and 4 is less than 5.

# Example 1:
# Input: nums = [3, 5, 2, 6], k = 2
# Output: [2, 6]
# Explanation: Among the set of every possible
# subsequence: {[3, 5], [3, 2], [3, 6], [5, 2], [5, 6], [2, 6]}, [2, 6] is the most competitive.

# Example 2:
# Input: nums = [2, 4, 3, 3, 5, 4, 9, 6], k = 4
# Output: [2, 3, 3, 4]

# Constraints:

# 1 <= nums.length <= 105
# 0 <= nums[i] <= 109
# 1 <= k <= nums.length

def most_competitive(nums: list[int], k: int) -> list[int]:
    # array's length:
    n = len(nums)
    # result array:
    res = []
    # decreasing monotonic stack:
    m_stack = deque()
    # the core cycle:
    i = 0
    while i < n:
        # appends an element to the monotonic stack:
        append_an_el_to_mono_d_stack(m_stack, nums[i])
        if i >= n - k:
            res += [m_stack[0]]
            m_stack.popleft()
        i += 1
    # returns res:
    return res


def append_an_el_to_mono_d_stack(m_stack: deque, el: int) -> None:
    while len(m_stack) > 0 and m_stack[-1] > el:
        m_stack.pop()
    m_stack += [el]


test_ex = [2, 7, 3, 6, 8, 5, 2, 6, 4], 6

test_ex_1 = [2, 4, 3, 3, 5, 4, 9, 6], 4

print(f'test ex res -> {most_competitive(*test_ex)}')
print(f'test ex 1 res -> {most_competitive(*test_ex_1)}')                             # 36 366 98 989 98989 LL
