import math
import random
import sys
import time

import arcade


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

    def set_child(self, is_left: bool, node_: 'Node') -> None:
        if is_left:
            self.left_node = node_
        else:
            self.right_node = node_

    def set_parent(self, node_: 'Node'):
        self.parent = node_

    def get_min_node(self) -> int:
        """inorder-successor search"""
        current = self
        # Let's find the last right node - it will be the inorder-successor:
        while current.left_node is not None:
            current = current.left_node
        return current

    def __str__(self):
        return f'[{self.val}, {self.weight}]'

    def __repr__(self):
        return str(self)


class BIST:
    """Binary searching tree with indexation"""

    def __init__(self):
        self.root = None
        self.elements_occurred = set()

    def insert(self, val: int, balance=True) -> int:
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
        return self.root.weight - counter_ - 1

    def delete_by_val(self, value: int) -> None:

        def delete_node(root: 'Node', val: int) -> 'Node' or None:
            """deletes a node with the value = val"""
            if root is not None:
                root.weight -= 1  # weight decreasing while descending
            if root is None:
                # if the tree is empty:
                return
            # let us find the node which should be deleted:
            if val > root.val:
                root.right_node = delete_node(root.right_node, val)
            elif val < root.val:
                root.left_node = delete_node(root.left_node, val)
            else:
                # if the node has one or no children:
                if root.left_node is None:
                    temp = root.right_node
                    return temp
                elif root.right_node is None:
                    temp = root.left_node
                    return temp
                # if the node has two children, then we locate the centred successor
                # at the place of the current node...
                temp = root.right_node.get_min_node()
                root.val = temp.val
                # removing the inorder-successor:
                root.right_node = delete_node(root.right_node, temp.val)
            # returns the root:
            return root

        # checks if there is such element in the BIST:
        if value not in self.elements_occurred:
            raise ValueError(f'there is no such an element in the BIST...')
        # inner rec method call:
        self.root = delete_node(self.root, value)
        # removing val from the set:
        self.elements_occurred.remove(value)

    def delete_by_index(self, ind: int):
        ...

    def get(self, ind: int) -> 'Node':
        """gets value of the node by its index"""
        # check:
        if ind < 0 or ind >= len(self.elements_occurred):
            raise ValueError(f'there is no element with such an index in BIST!')
        # main logic:
        node_ = self.root
        counter_ = 0
        while True:
            # print(f'node_: {node_}, counter_: {counter_}, left subtree weight: {"empty" if node_.left_node is None else node_.left_node.weight}')
            left_subtree_weight = self.get_weight(node_.left_node)
            if counter_ + left_subtree_weight < ind:
                counter_ += 1 + left_subtree_weight
                node_ = node_.right_node
            elif counter_ + left_subtree_weight > ind:
                node_ = node_.left_node
            else:
                return node_

    def index(self, val: int):
        """returns the index of the node with the val given"""
        if val not in self.elements_occurred:
            raise ValueError(f'there is no element with such a value in BIST!')
        # main logic:
        node_ = self.root
        counter_ = 0
        while True:
            left_subtree_weight = self.get_weight(node_.left_node)
            if node_.val < val:
                counter_ += 1 + left_subtree_weight
                node_ = node_.right_node
            elif node_.val > val:
                node_ = node_.left_node
            else:
                return counter_ + left_subtree_weight

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

    def build_balanced_bist(self, nodes, m):
        """recursive func for building height-balanced BIST from the sorted list of nodes given"""
        def build_balanced_bist(start, end):
            # base case:
            if start > end or start == end == m:
                return None, 0
            # pivot index:
            mid = (start + end) // 2
            # root is the middle node:
            # print(f'start, end: {start, end} mid: {mid}')
            root = nodes[mid]
            # adding the node's val to the set:
            self.elements_occurred.add(root.val)
            # builds the left and the right subtrees recursively:
            root.left_node, wl = build_balanced_bist(start, mid - 1)
            root.right_node, wr = build_balanced_bist(mid + 1, end)
            # defines important nodes' pars:
            if root.left_node is not None:
                root.left_node.parent = root
                root.left_node.is_left = True
            if root.right_node is not None:
                root.right_node.parent = root
                root.right_node.is_left = False
            root.weight = 1 + wl + wr
            # returns the root node and its weight as tuple:
            return root, root.weight
        # calls the inner core func:
        self.root = build_balanced_bist(0, m)[0]

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
                print(f'{node_}', end=' -> ')
                inorder(node_.right_node)

        inorder(self.root)
        print()

    @property
    def depth(self) -> int:
        return ...

    @property
    def size(self) -> int:
        return 0 if self.root is None else self.root.weight


# bist = BIST()
# print(bist.insert(1))
# print(bist.insert(2))
# print(bist.insert(3))
# print(bist.insert(4))
# print(bist.insert(5))
# print(bist.insert(6))
# print(bist.insert(7))
# print(bist.insert(8))
# print(bist.insert(9))
# print(bist.insert(989))
# print(bist.insert(98))
# print(bist.insert(0))
# print(bist.insert(89))
#
# bist.inorder()
#
# el = 98
#
# print(f'index of {el} is: {bist.index(el)}')

# m = 300_000
# array = [_ for _ in range(1, m)]
# random.shuffle(array)
# start = time.time_ns()
# for _ in array:  # range(1, m):
#     # print(f'{_} inserting...')
#     # bist.insert(_, balance=True)
#     g = _ ** 2
# print(f'size: {sys.getsizeof(bist.root)}')
# finish = time.time_ns()
# print(f'time elapsed: {(finish - start) // 10 ** 6} milliseconds')
# bist.inorder()


# bist.insert(7)
# bist.insert(5)
# bist.insert(13)
# bist.insert(3)
# bist.insert(2)
# bist.insert(10)
# bist.insert(8)
# bist.insert(17)
# bist.insert(12)
# bist.insert(15)
# bist.insert(16)
# bist.insert(98)
# bist.inorder()
# bist.delete_by_value(13)
# bist.inorder()
# print(f'el: {bist.get(8)}')
# bist.inorder()
# print(f'el: {bist.get(11)}')
# print(f'el: {bist.get(6)}')

# m = 3 * 100_000 + 1
#
# array = [_ for _ in range(1, m)]
# random.shuffle(array)
# start = time.time_ns()
# for el_ in array:
#     bist.insert(el_)
# finish = time.time_ns()
# print(f'time elapsed: {(finish - start) // 10 ** 6} milliseconds')
#
# start = time.time_ns()
# for i in range(m):
#     bist.get(random.randint(1, m))
# finish = time.time_ns()
# print(f'time elapsed: {(finish - start) // 10 ** 6} milliseconds')


# screen sizes:
SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1050


class ApplicationBIST(arcade.Window):
    def __init__(self, width, height):
        super().__init__(width, height)
        arcade.set_background_color(arcade.color.DUTCH_WHITE)
        # the BIST tree:
        self.bist = BIST()
        # self

    def setup(self):
        ...

    def update(self, delta_time: float):
        ...

    def on_draw(self):
        # renders this screen:
        arcade.start_render()

    def on_mouse_motion(self, x: int, y: int, dx: int, dy: int):
        ...

    def on_mouse_press(self, x: int, y: int, button: int, modifiers: int):
        ...

    def on_key_press(self, symbol: int, modifiers: int):
        ...

    def on_key_release(self, symbol: int, modifiers: int):
        ...




# TODO: 1. Arcade representation of a simple BIST structure...
# TODO: 2. Tree self-balancing...
