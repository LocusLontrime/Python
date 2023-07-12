# accepted on coderun
# Tree:
import math


class Node:
    def __init__(self, val: int, parent=None):
        # key or value (data) of the node:
        self.val = val
        # children (leafs):
        self.parent = parent
        self.left_node = None
        self.right_node = None
        # weight (auxiliary par, used for index defining):
        self.weight = 1

    def get_min_node(self) -> int:
        """inorder-successor search"""
        current = self
        # Let's find the last right node - it will be the inorder-successor:
        while current.left_node is not None:
            current = current.left_node
        return current


class BIST:
    """Binary searching tree with indexation"""

    def __init__(self):
        self.root = None
        self.elements_occurred = set()

    def insert(self, val: int, balance: bool = True) -> int:
        # print(f'ADDING {val}...')
        # adding the val to the set:
        self.elements_occurred.add(val)
        # root check:
        if self.root is None:
            # print(f"the root has been changed! Now the root's val is: {val}")
            self.root = Node(val)
            return 0
        # the main algo:
        node_ = self.root
        counter_ = 0
        while True:
            node_.weight += 1
            left_subtree_weight = self.get_weight(node_.left_node)
            # print(f'node_: {node_}')
            if node_.val < val:
                counter_ += 1 + left_subtree_weight
                if node_.right_node is None:
                    node_inserted = node_.right_node = Node(val, node_)
                    break
                node_ = node_.right_node
            else:
                if node_.left_node is None:
                    node_inserted = node_.left_node = Node(val, node_)
                    break
                node_ = node_.left_node
        # print(f'{val} successfully added to the BIST')
        if balance:
            self.balance(node_inserted)
        # returns the index of the element in the array sorted in descending order:
        return counter_  # self.root.weight - counter_ - 1

    def get(self, ind: int) -> 'Node':
        """gets value of the node by its index"""
        # check:
        if ind < 0 or ind >= len(self.elements_occurred):
            raise ValueError(f'there is no element with such an index in BIST!')
        # main logic:
        node_ = self.root
        counter_ = 0
        while True:
            left_subtree_weight = self.get_weight(node_.left_node)
            if counter_ + left_subtree_weight < ind:
                counter_ += 1 + left_subtree_weight
                node_ = node_.right_node
            elif counter_ + left_subtree_weight > ind:
                node_ = node_.left_node
            else:
                return node_

    def balance(self, node_: 'Node'):
        # cycle of rotations:
        # print(f"now the {node_}'s sub tree is being balanced...")
        while True:
            # left and right subtrees' weights comparison:
            left_depth = self.get_quasi_depth(node_.left_node)
            right_depth = self.get_quasi_depth(node_.right_node)                      # 36.6 98
            if left_depth > right_depth + 1:
                # right rotation:
                child = node_.left_node
                parent = node_.parent

                if parent is not None:
                    if parent.right_node == node_:
                        parent.right_node = child
                    elif parent.left_node == node_:
                        parent.left_node = child
                else:
                    self.root = child
                child.parent = parent
                node_.parent = child

                node_.left_node = child.right_node
                if node_.left_node is not None:
                    node_.left_node.parent = node_

                child.right_node = node_

                node_.weight = self.weight_recalc(node_)  # 1 + self.get_weight(node_.left_node) + self.get_weight(node_.right_node)
                child.weight = self.weight_recalc(child)  # 1 + self.get_weight(child.left_node) + self.get_weight(child.right_node)

                node_ = child
            elif right_depth > left_depth + 1:
                # left rotation:
                child = node_.right_node
                parent = node_.parent

                if parent is not None:
                    if parent.right_node == node_:
                        parent.right_node = child
                    elif parent.left_node == node_:
                        parent.left_node = child
                else:
                    self.root = child
                child.parent = parent
                node_.parent = child

                node_.right_node = child.left_node
                if node_.right_node is not None:
                    node_.right_node.parent = node_

                child.left_node = node_

                node_.weight = self.weight_recalc(node_)  # 1 + self.get_weight(node_.left_node) + self.get_weight(node_.right_node)
                child.weight = self.weight_recalc(child)  # 1 + self.get_weight(child.left_node) + self.get_weight(child.right_node)

                node_ = child

            if node_.parent is not None:
                node_ = node_.parent
            else:
                break

    def weight_recalc(self, node_: 'Node') -> int:
        return 1 + self.get_weight(node_.left_node) + self.get_weight(node_.right_node)

    @staticmethod
    def get_weight(node_: 'Node'):
        return 0 if node_ is None else node_.weight

    @staticmethod
    def get_quasi_depth(node_: 'Node') -> int:
        if node_ is None:
            return 0

        if node_.weight == 1:
            return 1
        elif node_.weight == 2:
            return 2

        depth = math.log2(node_.weight + 1)
        return int(depth) if depth % 1 == 0.0 else math.ceil(depth)


def sum_medians():
    n, array = get_pars()
    bit_tree = BIST()
    sum_ = 0
    for i in array:
        bit_tree.insert(i)
        length_ = bit_tree.root.weight
        el_ = bit_tree.get(length_ // 2 - 1) if length_ % 2 == 0 else bit_tree.get((length_ + 1) // 2 - 1)
        sum_ += el_.val
        # print(f'{length_}. el_: {el_.val}, sum_: {sum_}')
    print(f'{sum_}')


def get_pars():
    n = int(input())
    array = list(map(int, input().split()))
    return n, array



