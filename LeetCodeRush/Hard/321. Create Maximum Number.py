# You are given two integer arrays nums1 and nums2 of lengths m and n respectively.
# nums1 and nums2 represent the digits o two numbers.You are also given an integer k.
from collections import deque


# Create the maximum number of length k <= m + n from digits of the two numbers.
# The relative order of the digits from the same array must be preserved.

# Return an array of the k digits representing the answer.

# Example 1:
# Input: nums1 = [3, 4, 6, 5], nums2 = [9, 1, 2, 5, 8, 3], k = 5
# Output: [9, 8, 6, 5, 3]

# Example 2:
# Input: nums1 = [6, 7], nums2 = [6, 0, 4], k = 5
# Output: [6, 7, 6, 0, 4]

# Example 3:
# Input: nums1 = [3, 9], nums2 = [8, 9], k = 3
# Output: [9, 8, 9]

# Constraints:
# m == nums1.length
# n == nums2.length
# 1 <= m, n <= 500
# 0 <= nums1[i], nums2[i] <= 9
# 1 <= k <= m + n
# nums1 and nums2 do not have leading zeros.

def max_number(nums1: list[int], nums2: list[int], k: int) -> list[int]:
    print(f'{nums1 = }')
    print(f'{nums2 = }')
    nums1_ = [(el, i) for i, el in enumerate(nums1)]
    nums2_ = [(el, i) for i, el in enumerate(nums2)]
    seq_len = 0
    iteration = 0
    indices_1_to_merge = set()
    indices_2_to_merge = set()
    # let use some monotonic deque tactics:
    while nums1_ and nums2_:
        print(f'{iteration} step ->')
        q1 = monotonic_deque(nums1_)
        q2 = monotonic_deque(nums2_)
        seq_len += len(q1) + len(q2)
        # new nums1 and nums 2:
        set1 = {i for _, i in q1}
        set2 = {i for _, i in q2}
        indices_1_to_merge |= set1
        indices_2_to_merge |= set2
        print(f'{set1 = }')
        print(f'{set2 = }')
        print(f'{indices_1_to_merge = }')
        print(f'{indices_2_to_merge = }')
        # check for k:
        if k <= seq_len:
            # let us merge this:
            arr1_to_merge = [_ for i, _ in enumerate(nums1) if i in indices_1_to_merge]
            arr2_to_merge = [_ for i, _ in enumerate(nums2) if i in indices_2_to_merge]
            print(f'{arr1_to_merge = }')
            print(f'{arr2_to_merge = }')
            return merge(arr1_to_merge, arr2_to_merge, k)
        nums1_ = [(_, i) for _, i in nums1_ if i not in set1]
        nums2_ = [(_, i) for _, i in nums2_ if i not in set2]
        print(f'nums1 after -> {nums1_}')
        print(f'nums2 after -> {nums2_}')


def monotonic_deque(arr: list[tuple[int, int]]) -> deque:
    # array's length:
    n = len(arr)
    q = deque()
    for i in range(n):
        while len(q) > 0 and q[-1][0] < arr[i][0]:
            q.pop()
        q.append(arr[i])
    print(f'{q = }')
    return q


def merge(arr1: list[int], arr2: list[int]) -> list[int]:
    res = []
    i1, i2 = 0, 0
    # common merging:
    while i1 < len(arr1) and i2 < len(arr2):
        nums1_el_greater, d = step_up(arr1, arr2, i1, i2)
        if nums1_el_greater:
            res += [arr1[_] for _ in range(i1, i1 + d)]
            i1 += d
        else:
            res += [arr2[_] for _ in range(i2, i2 + d)]
            i2 += d
    # rem merging:
    while i1 < len(arr1):
        res += [arr1[i1]]
        i1 += 1

    while i2 < len(arr2):
        res += [arr2[i2]]
        i2 += 1

    return res


def step_up(arr1: list[int], arr2: list[int], i1, i2) -> tuple[bool, int]:
    delta = 0
    res = None
    while i1 + delta < len(arr1) and i2 + delta < len(arr2):
        if arr1[i1 + delta] == arr2[i2 + delta]:
            delta += 1
        else:
            return arr1[i1 + delta] > arr2[i2 + delta], delta + 1


test_ex = [3, 4, 6, 5], [9, 1, 2, 5, 8, 3], 5 + 1

print(f'test ex res -> {max_number(*test_ex)}')                                       # 36 366 98989 98989 LL
