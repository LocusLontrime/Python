# accepted on coderun
import sys
import math
from collections import defaultdict as d


class Node:
    def __init__(self, val: int, pid: int, pg: int, parent=None):
        # key or value (data) of the node:
        self.val = val
        # children (leafs):
        self.parent = parent
        self.left_node = None
        self.right_node = None
        # weight (auxiliary par, used for index defining):
        self.weight = 1
        # task pars:
        self.pid = pid
        self.pg = pg

    def __str__(self):
        return f'{self.pid}'  # f'[{self.val}, {self.weight}]({self.pid}, {self.pg})'

    def __repr__(self):
        return str(self)


class BIST:
    """Binary searching tree with indexation"""

    def __init__(self):
        self.root = None
        self.elements_occurred = set()

    def insert(self, val: int, pid: int, pg: int, balance=True) -> int:
        # print(f'ADDING {val}...')
        # adding the val to the set:
        self.elements_occurred.add(val)
        # root check:
        if self.root is None:
            # print(f"the root has been changed! Now the root's val is: {val}")
            self.root = Node(val, pid, pg)
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
                    node_inserted = node_.right_node = Node(val, pid, pg, node_)
                    break
                node_ = node_.right_node
            else:
                if node_.left_node is None:
                    node_inserted = node_.left_node = Node(val, pid, pg, node_)
                    break
                node_ = node_.left_node
        # print(f'{val} successfully added to the BIST')
        if balance:
            self.balance(node_inserted)
        # returns the index of the element in the array sorted in ascending order:
        return counter_  # self.root.weight - counter_ - 1

    def balance(self, node_: 'Node'):
        # cycle of rotations:
        # print(f"now the {node_}'s subtree is being balanced...")
        while True:
            # left and right subtrees' weights comparison:
            left_depth = self.get_quasi_depth(node_.left_node)
            right_depth = self.get_quasi_depth(node_.right_node)
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

                node_.weight = self.weight_recalc(
                    node_)  # 1 + self.get_weight(node_.left_node) + self.get_weight(node_.right_node)
                child.weight = self.weight_recalc(
                    child)  # 1 + self.get_weight(child.left_node) + self.get_weight(child.right_node)

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

                node_.weight = self.weight_recalc(
                    node_)  # 1 + self.get_weight(node_.left_node) + self.get_weight(node_.right_node)
                child.weight = self.weight_recalc(
                    child)  # 1 + self.get_weight(child.left_node) + self.get_weight(child.right_node)

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

    def inorder(self):
        def inorder(node_: 'Node'):
            if node_ is not None:
                inorder(node_.left_node)
                print(f'{node_}', end=' ')
                inorder(node_.right_node)

        inorder(self.root)


def validate_permutation():
    n, products_group = get_pars()
    start_ind_ = n  # bucket size = n
    sorted_groups = sorted(products_group.keys(), key=lambda x: len(products_group[x]), reverse=True)
    mkq = len(products_group[sorted_groups[0]])
    max_ind = n * mkq
    b_tree = BIST()
    ind_ = n
    for group_ in sorted_groups:
        for i_, pid_ in enumerate(products_group[group_]):
            b_tree.insert(ind_, pid_, group_)
            ind_ += n
            if ind_ >= max_ind + (n if len(products_group[group_]) == mkq else 0):
                start_ind_ += 1
                ind_ = start_ind_
    b_tree.inorder()


def get_pars():
    n = int(input())
    products_group = d(list)
    for _ in range(n):
        pid_, pc_ = input().split()  # map(int, input().split())
        products_group[pc_].append(pid_)
    return n, products_group


def main():
    validate_permutation()


if __name__ == '__main__':
    main()
