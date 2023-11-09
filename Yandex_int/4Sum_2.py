# n454 from leetcode.com
# accepted on leetcode.com (beats 70%)
from collections import defaultdict as d


def _4sum2(nums1: list[int], nums2: list[int], nums3: list[int], nums4: list[int]):  # 36 366 98 989 98989 LL
    nums12_sums = d(int)
    nums34_sums = d(int)
    for num1, num3 in zip(nums1, nums3):
        for num2, num4 in zip(nums2, nums4):
            nums12_sums[num1 + num2] += 1
            nums34_sums[num3 + num4] += 1
    res = 0
    for k, v in nums12_sums.items():
        res += v * nums34_sums[-k]
    return res


# Example:
nums1_ = [1, 2]
nums2_ = [-2, -1]
nums3_ = [-1, 2]
nums4_ = [0, 2]

nums1_x = [0]
nums2_x = [0]
nums3_x = [0]
nums4_x = [0]

print(f'_4sum2: {_4sum2(nums1_x, nums2_x, nums3_x, nums4_x)}')





