# accepted on codewars.com
max_depth = 0


class TreeNode:
    def __init__(self, value, left=None, right=None):
        self.value = value
        self.left = left
        self.right = right


def is_perfect(tree: TreeNode) -> bool:
    global max_depth
    max_depth = 0
    return dfs(tree, 0) == 2 ** max_depth - 1


def dfs(node: TreeNode, depth: int) -> int:
    global max_depth
    max_depth = max(max_depth, depth)
    if node is None:
        return 0
    else:
        return 1 + dfs(node.left, depth + 1) + dfs(node.right, depth + 1)


tree_ = TreeNode('A',
                 TreeNode('B',
                          TreeNode('D'),
                          TreeNode('E')
                          ),
                 TreeNode('C',
                          TreeNode('F'),
                          TreeNode('G')
                          )
                 )

print(f'is_perfect: {is_perfect(tree_)}')
