# Tree:
import math
import time
from functools import reduce
from itertools import count


class Node:
    def __init__(self, val: int, parent=None, freq: int = 1):
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
        return current.val


class BIST:
    """Binary searching tree with indexation"""

    def __init__(self):
        self.root = None
        self.elements_occurred = set()

    def insert(self, val: int, freq: int, balance: bool = True) -> int:
        # print(f'ADDING {val}...')
        # adding the val to the set:
        self.elements_occurred.add(val)
        # root check:
        if self.root is None:
            # print(f"the root has been changed! Now the root's val is: {val}")
            self.root = Node(val, freq=freq)
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
                    node_inserted = node_.right_node = Node(val, node_, freq)
                    break
                node_ = node_.right_node
            else:
                if node_.left_node is None:
                    node_inserted = node_.left_node = Node(val, node_, freq)
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

    def get_min(self) -> int:
        return self.root.get_min_node()

    def balance(self, node_: 'Node'):
        # cycle of rotations:
        # print(f"now the {node_}'s sub tree is being balanced...")
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


# accepted on codewars.com
def golomb(given, n):
    els_ = []
    temp_n = n
    si = 0
    # 0-case processing:
    if (g1 := next(giter := iter(given))) == 0:
        g2 = next(giter)
        if g2 == 1:
            g3 = next(giter)
            els_ += (addition := [g2, g3, g2, g1] + [g2 for _ in range(g3 - 2)])[: min(temp_n, len(addition))]
            if temp_n <= len(addition):
                return els_
            temp_n -= len(addition)
            si = 3
        else:
            els_ += (addition := [g2, g2] + [g1 for _ in range(g2)] + [g2 for _ in range(g2 - 2)])[: min(temp_n, len(addition))]
            if temp_n <= len(addition):
                return els_
            temp_n -= len(addition)
            si = 2
    # usual part:
    for i, _el in enumerate(giter if si else given, si):
        if len(els_) <= i:
            els_ += [_el for _ in range(min(_el, temp_n))]
            if _el >= temp_n:
                break
            temp_n -= _el
        else:
            els_ += [_el for _ in range(min(els_[i], temp_n))]
            if els_[i] >= temp_n:
                break
            temp_n -= els_[i]
    # returns result:
    return els_


class Iterable:
    def __init__(self, fn): self.fn = fn

    def __iter__(self): return self.fn()


iterable = lambda *fns: Iterable(lambda: (reduce(lambda z, fn: lambda v: fn(z(v)), fns)(i) for i in count(0)))

id_ = lambda x: x
plus = lambda v: lambda w: v + w
times = lambda v: lambda w: v * w
exp = lambda v: lambda w: v ** w
triangle = lambda x: x * (x + 1) // 2
square = lambda x: x * x

given_x = iterable(plus(1))
given_e = iterable(exp(2))
given_id = iterable(id_)

given_ = [1, 2, 4, 8, 16]

print(f'res: {golomb(given_id, 9)}')
