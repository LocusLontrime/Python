# accepted on leetcode.com

# Definition for a binary tree node.
import math
from typing import Optional


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class Solution:
    MIN_ = -4 * 10 ** 4 - 1
    MAX_ = 4 * 10 ** 4 + 1

    max_sum = -math.inf

    def max_sum_BST(self, root: Optional[TreeNode]) -> int:
        Solution.max_sum = -math.inf
        # let use some recursion:
        self.rec_core(root)
        return max(Solution.max_sum, 0)

    def rec_core(self, node: Optional[TreeNode]):
        # base case:
        if node is None:
            return 0, True, Solution.MAX_, Solution.MIN_, Solution.MAX_, Solution.MIN_
        # body of rec:
        sum_left, is_bst_left, min_left_left, max_left_left, min_right_left, max_right_left = self.rec_core(node.left)
        sum_right, is_bst_right, min_left_right, max_left_right, min_right_right, max_right_right = self.rec_core(
            node.right)
        # print(f'{node.val = }')
        # print(f'{sum_left, is_bst_left, min_left_left, max_left_left, min_right_left, max_right_left = }')
        # print(f'{sum_right, is_bst_right, min_left_right, max_left_right, min_right_right, max_right_right = }')
        # main logic:
        sum_ = sum_left + node.val + sum_right
        is_bst = is_bst_left and is_bst_right and (max_right_left < node.val < min_left_right)
        if is_bst:
            Solution.max_sum = max(Solution.max_sum, sum_)
            # returns pars:
        return (sum_, is_bst,
                min(min_left_left, node.val),
                max(max_right_left, node.val),
                min(min_left_right, node.val),
                max(max_right_right, node.val)                                        # 36 366 98 989 98989 LL LL
                )
