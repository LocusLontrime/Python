# accepted on coderun
import sys
import math


class Node:
    def __init__(self, a: int, b: int, id_: int, parent=None):
        # key or value (data) of the node:
        self.a = a
        self.b = b
        self.id = id_
        # children (leafs):
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

    @property
    def val(self):
        return self.b - self.a, self.id

    @property
    def pars(self):
        return self.a, self.b, self.id

    def __lt__(self, other):
        return self.val < other.val


class BIST:
    """Binary searching tree with indexation"""

    def __init__(self):
        self.root = None

    def insert(self, a: int, b: int, id_: int) -> tuple[int, Node]:
        # adding the val to the set:
        node = Node(a, b, id_)
        # root check:
        if self.root is None:
            self.root = node
            return 0, self.root
        # the main algo:
        node_ = self.root
        counter_ = 0
        while True:
            node_.weight += 1
            left_subtree_weight = self.get_weight(node_.left_node)
            if node_.val < node.val:
                counter_ += 1 + left_subtree_weight
                if node_.right_node is None:
                    node_inserted = node_.right_node = Node(a, b, id_, node_)
                    break
                node_ = node_.right_node
            else:
                if node_.left_node is None:
                    node_inserted = node_.left_node = Node(a, b, id_, node_)
                    break
                node_ = node_.left_node
        # returns the index of the element in the array sorted in descending order:
        return self.root.weight - counter_ - 1, node_inserted

    def delete_by_val(self, value: tuple[int, int]) -> None:

        def delete_node(root: 'Node', val: tuple[int, int]) -> 'Node' or None:
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
                    return root.right_node
                elif root.right_node is None:
                    return root.left_node
                # if the node has two children, then we locate the centred successor
                # at the place of the current node...
                temp = root.right_node.get_min_node()
                root.a = temp.f_set
                root.b = temp.b
                root.id = temp.id
                # removing the inorder-successor:
                root.right_node = delete_node(root.right_node, temp.val)
            # returns the root:
            return root

        # inner rec method call:
        self.root = delete_node(self.root, value)

    def get(self, ind: int) -> 'Node':
        """gets value of the node by its index (descending order)"""
        ind = self.root.weight - ind - 1
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

    def index(self, val: tuple[int, int]):
        """returns the index of the node with the val given"""
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
                return self.root.weight - 1 - (counter_ + left_subtree_weight)

    def build_balanced_bist(self, nodes, m):
        """recursive func for building height-balanced BIST from the sorted list of nodes given"""

        def build_balanced_bist(start, end):
            # base case:
            if start > end or start == end == m:
                return None, 0
            # pivot index:
            mid = (start + end) // 2
            # root is the middle node:
            root = nodes[mid]
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

    @staticmethod
    def get_weight(node_: 'Node'):
        return 0 if node_ is None else node_.weight


def max_sums():
    n, a, b, m, certs = get_pars()
    # shaping the list of nodes:
    students = [Node(a[i], b[i], i) for i in range(n)]
    sorted_students = sorted(students)
    # border index of n // 2 larger elems:
    bord_ind = n // 2 - 1
    sum_a = sum(st.a for st in students)
    sum_b_minus_a = sum(st.b - st.a for ind, st in enumerate(sorted_students) if ind > bord_ind)
    # now building the BIST tree:
    b_tree = BIST()
    b_tree.build_balanced_bist(sorted_students, len(students))
    del sorted_students
    # processing the queries:
    for ind_, type_, d_ in certs:
        stud_a, stud_b, stud_id = students[ind_ - 1].pars
        stud_val = stud_b - stud_a, stud_id
        da_, db_ = (d_, 0) if type_ == 1 else (0, d_)
        # getting the index in descending order of stud_:
        _ind = b_tree.index(stud_val)
        # now inserting the new_stud_ and applying the appropriate changes:         
        sum_a += da_
        if _ind <= bord_ind:
            sum_b_minus_a -= stud_b - stud_a  # 36.6 98
            border_stud_ = b_tree.get(bord_ind + 1)
            sum_b_minus_a += border_stud_.b - border_stud_.a
            # carefully removing the old stud_:
        b_tree.delete_by_val(stud_val)
        # appending a new stud_ to the BIST:
        new_ind_, new_stud_ = b_tree.insert(stud_a + da_, stud_b + db_, stud_id)
        if new_ind_ <= bord_ind:
            sum_b_minus_a += new_stud_.b - new_stud_.a
            border_stud_ = b_tree.get(bord_ind + 1)
            sum_b_minus_a -= border_stud_.b - border_stud_.a
        students[ind_ - 1] = new_stud_
        # printing the interim result:
        print(f'{sum_a + sum_b_minus_a}')


def get_pars() -> tuple[int, list[int], list[int], int, list[tuple[int, ...]]]:
    n = int(input())
    a = [int(_) for _ in input().split(' ')]
    b = [int(_) for _ in input().split(' ')]
    m = int(input())
    certs = [tuple(int(_) for _ in input().split()) for _ in range(m)]
    return n, a, b, m, certs


def main():
    max_sums()


if __name__ == '__main__':
    main()
