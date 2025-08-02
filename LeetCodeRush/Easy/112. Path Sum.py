# accepted on leetcode.com

# Given the root of a binary tree and an integer targetSum,
# return true if the tree has a root-to-leaf path such that adding up all the values along the path equals targetSum.

# A leaf is a node with no children.


# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def has_path_sum(node: TreeNode | None, target_sum: int) -> bool:  # dfs
    # border cases:
    if node is None:
        return False
    if node.left is None and node.right is None:
        return target_sum == node.val
    # recurrent relation:
    return has_path_sum(node.left, target_sum - node.val) | has_path_sum(node.right, target_sum - node.val)




