class Node:
    def __init__(self, weight: int, left: 'Node' = None, right: 'Node' = None):
        self.weight = weight
        self.left_child = left
        self.right_child = right


class BinTree:
    def __init__(self, root: Node):
        self.root = root

    def max_path(self) -> int:
        def rec_core(node_: 'Node') -> int:
            # border case:
            if node_ is None:
                return 0
            # recurrent relation:
            return max(rec_core(node_.left_child), rec_core(node_.right_child)) + node_.weight

        return rec_core(self.root)


root_ = Node(11,
             Node(8,
                  Node(1,
                       Node(17),
                       Node(2)
                       ),
                  Node(11,
                       Node(7))
                  ),
             Node(7,
                  Node(22,
                       right=Node(1)),
                  Node(19,
                       right=Node(13))
                  )
             )

bin_tree = BinTree(root_)


print(f'max path: {bin_tree.max_path()}')
