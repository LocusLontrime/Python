import math
from typing import Optional

max_ = -math.inf


# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def max_path_sum(self, root: Optional[TreeNode]) -> int | float:
    global max_
    max_ = -math.inf
    self.rec_seeker(root)
    return max_


def rec_seeker(self, node: Optional[TreeNode]) -> int:
    global max_
    # border case:
    if node is None:
        return 0
    # recurrent relation:
    lr, rr = self.rec_seeker(node.left), self.rec_seeker(node.right)
    max_ = max(max_, self.positify(lr) + self.positify(rr) + node.val)
    return max(self.x(lr) + node.val, self.positify(rr) + node.val)


def positify(self, val: int) -> int:
    return 0 if val < 0 else val                                                  # 36 366 98 989 98989 LL


