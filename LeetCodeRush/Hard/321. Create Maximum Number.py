# accepted on leetcode.com

# You are given two integer arrays nums1 and nums2 of lengths m and n respectively.
# nums1 and nums2 represent the digits o two numbers.You are also given an integer k.

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

def max_number(self, nums1: list[int], nums2: list[int], k: int) -> list[int]:
    print(f'{nums1 = }')
    print(f'{nums2 = }')
    # arrays' lengths:
    n1, n2 = len(nums1), len(nums2)
    # the core cycle (let k1 + k2 = k):
    max_num = []
    for k1 in range(max(0, k - n2), min(k, n1) + 1):
        k2 = k - k1
        print(f'{k1, k2 = }')
        num1_most_comp_subseq_k1_length = self.most_competitive(nums1, k1)
        num2_most_comp_subseq_k2_length = self.most_competitive(nums2, k2)
        print(f'...{num1_most_comp_subseq_k1_length = }')
        print(f'...{num2_most_comp_subseq_k2_length = }')
        interim_res = self.largest_merge(num1_most_comp_subseq_k1_length, num2_most_comp_subseq_k2_length)
        print(f'---> {interim_res = }')
        max_num = max(max_num, interim_res)
    return max_num

    # 1673 the most competitive subseq leetcode.com


def most_competitive(self, nums: list[int], k: int) -> list[int]:
    # array's length:
    n = len(nums)
    # decreasing monotonic stack:
    m_stack = []
    # the core cycle:
    i = 0
    drops_rem = n - k
    while i < n:
        # appends an element to the monotonic stack:
        while drops_rem and len(m_stack) > 0 and m_stack[-1] < nums[i]:
            m_stack.pop()
            drops_rem -= 1
        m_stack += [nums[i]]
        i += 1
    # returns res:
    return m_stack[:k]


# 1754 largest merge of 2 strs leetcode.com
def largest_merge(self, num1: list[int], num2: list[int]) -> list[int]:
    a = list(num1)
    b = list(num2)
    res = []
    while a and b:
        if a > b:
            res.append(a[0])
            a.pop(0)
        else:
            res.append(b[0])
            b.pop(0)
    return res + a + b


test_ex = [3, 4, 6, 5], [9, 1, 2, 5, 8, 3], 5 + 1

print(f'test ex res -> {max_number(*test_ex)}')                                       # 36 366 98989 98989 LL
