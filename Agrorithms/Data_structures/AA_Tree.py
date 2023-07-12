class AaTreeSet:

    def __init__(self, coll=None):
        self.clear()
        if coll is not None:
            for val in coll:
                self.add(val)

    def clear(self):
        self.root = AaTreeSet.Node.EMPTY_LEAF
        self.size = 0

    def __len__(self):
        return self.size

    def __contains__(self, val):
        node = self.root
        while node is not AaTreeSet.Node.EMPTY_LEAF:
            if val < node.value:
                node = node.left
            elif val > node.value:
                node = node.right
            else:
                return True
        return False

    def inorder(self):
        self.root.inorder()

    def add(self, val):
        print(f'element to be added: {val}')
        if val in self:
            return
        self.root, c_ = self.root.add(val)
        print(f'index: {c_}, root: {self.root}')
        self.size += 1

    def remove(self, val):
        self.root, found = self.root.remove(val)
        if not found:
            raise KeyError(str(val))
        self.size -= 1

    def discard(self, val):
        self.root, found = self.root.remove(val)
        if found:
            self.size -= 1

    # Note: Not fail-fast on concurrent modification.
    def __iter__(self):
        stack = []
        node = self.root
        while True:
            while node is not AaTreeSet.Node.EMPTY_LEAF:
                stack.append(node)
                node = node.left
            if len(stack) == 0:
                break
            node = stack.pop()
            yield node.value
            node = node.right

    # For unit tests
    def check_structure(self):
        visited = set()
        if self.root.check_structure(visited) != self.size or len(visited) != self.size:
            raise AssertionError()

    class Node:

        def __init__(self, val=None):
            self.value = val
            if val is None:  # For the singleton empty leaf node
                self.level = 0
            else:  # Normal non-leaf nodes
                self.level = 1
                self.left = AaTreeSet.Node.EMPTY_LEAF  # static member instead of None
                self.right = AaTreeSet.Node.EMPTY_LEAF
                # TODO: add: weight, ...
                self.weight = 1  # def weight for a leaf...

        def __str__(self):
            return f'[{self.value}, {self.weight}]'

        def __repr__(self):
            return str(self)

        def inorder(self):
            def inorder(node_):
                # print(f'node_: {node_}')
                if node_ != AaTreeSet.Node.EMPTY_LEAF:
                    inorder(node_.left)
                    print(f'{node_}', end=' -> ')
                    inorder(node_.right)

            inorder(self)
            print()

        def weight_recalc(self) -> None:
            self.weight = 1 + self.left.get_weight() + self.right.get_weight()

        def get_weight(self):
            return 0 if self is AaTreeSet.Node.EMPTY_LEAF else self.weight

        def add(self, val: int):
            # helps to calculate the index of the element added...
            counter = 0

            def add(node_) -> 'AaTreeSet.Node':
                nonlocal counter

                if node_ is AaTreeSet.Node.EMPTY_LEAF:
                    return AaTreeSet.Node(val)

                node_.weight += 1
                left_subtree_weight = node_.left.get_weight()

                # print(f'node_: {node_}, left_subtree_weight: {left_subtree_weight}')

                if val < node_.value:
                    node_.left = add(node_.left)
                elif val > node_.value:
                    node_.right = add(node_.right)
                    counter += 1 + left_subtree_weight
                else:
                    raise ValueError("Value already in tree")
                # print(f're-balancing...')
                return node_.skew().split()  # Re-balance this node

            return add(self), counter

        def remove(self, val):
            EMPTY = AaTreeSet.Node.EMPTY_LEAF
            if self is EMPTY:
                return EMPTY, False
            self.weight -= 1  # weight decreasing while descending
            if val < self.value:
                self.left, found = self.left.remove(val)
            elif val > self.value:
                self.right, found = self.right.remove(val)
            else:  # Remove value at this node
                found = True
                if self.left is not EMPTY:
                    # Find predecessor node
                    temp = self.left
                    while temp.right is not EMPTY:
                        temp = temp.right
                    self.value = temp.value  # Replace value with predecessor
                    self.left, fnd = self.left.remove(self.value)  # Remove predecessor node
                    assert fnd
                elif self.right is not EMPTY:
                    # Find successor node
                    temp = self.right
                    while temp.left is not EMPTY:
                        temp = temp.left
                    self.value = temp.value  # Replace value with successor
                    self.right, fnd = self.right.remove(self.value)  # Remove successor node
                    assert fnd
                else:
                    assert self.level == 1
                    return EMPTY, True

            # Rebalance this node if a child was lowered
            if not found or self.level == min(self.left.level, self.right.level) + 1:
                return self, found
            if self.right.level == self.level:
                self.right.level -= 1
            self.level -= 1
            result = self.skew()
            result.right = result.right.skew()
            if result.right.right is not EMPTY:
                result.right.right = result.right.right.skew()
            result = result.split()
            result.right = result.right.split()
            return result, True

        def pop_min(self):
            # gets the minimal value element and removes it from the aa_tree...
            ...

        #       |          |
        #   A - B    ->    A - B
        #  / \   \        /   / \
        # 0   1   2      0   1   2
        def skew(self):
            assert self is not AaTreeSet.Node.EMPTY_LEAF
            if self.left.level < self.level:
                return self
            result = self.left
            self.left = result.right
            result.right = self
            # recalc weight for result and self
            self.weight_recalc()
            result.weight_recalc()
            # returns res:
            return result

        #   |                      |
        #   |                    - B -
        #   |                   /     \
        #   A - B - C    ->    A       C
        #  /   /   / \        / \     / \
        # 0   1   2   3      0   1   2   3
        def split(self):
            assert self is not AaTreeSet.Node.EMPTY_LEAF
            # Must short-circuit because if right.level < self.level, then right.right might not exist
            if self.right.level < self.level or self.right.right.level < self.level:
                return self
            result = self.right
            self.right = result.left
            result.left = self
            result.level += 1
            # recalc weight for result and self
            self.weight_recalc()
            result.weight_recalc()
            # returns res:
            return result

        # For unit tests, invokable by the outer class.
        def check_structure(self, visited_nodes):
            if self is AaTreeSet.Node.EMPTY_LEAF:
                return 0
            if self in visited_nodes:
                raise AssertionError()
            visited_nodes.add(self)

            value = self.value
            level = self.level
            left = self.left
            right = self.right
            if value is None or left is None or right is None:
                raise AssertionError()
            if not (level > 0 and level == left.level + 1 and level - right.level in (0, 1)):
                raise AssertionError()
            if level == right.level and level == right.right.level:  # Must short-circuit evaluate
                raise AssertionError()
            if left != AaTreeSet.Node.EMPTY_LEAF and not (left.value < value):
                raise AssertionError()
            if right != AaTreeSet.Node.EMPTY_LEAF and not (right.value > value):
                raise AssertionError()

            size = 1 + left.check_structure(visited_nodes) + right.check_structure(visited_nodes)
            if not (2 ** level - 1 <= size <= 3 ** level - 1):
                raise AssertionError()
            return size


# Static initializer. A bit of a hack, but more elegant than using None values as leaf nodes.
AaTreeSet.Node.EMPTY_LEAF = AaTreeSet.Node()


aa_tree = AaTreeSet()
aa_tree.add(11)
aa_tree.add(16)
aa_tree.add(8)
aa_tree.add(12)
aa_tree.add(5)
aa_tree.add(7)
aa_tree.add(98)

aa_tree.remove(16)

print(f'root: {aa_tree.root}')
print(f'root.left: {aa_tree.root.left}')
print(f'root.right: {aa_tree.root.right}')
# print(f'root.left.left: {aa_tree.root.left.left}')
# print(f'root.left.right: {aa_tree.root.left.right}')
print(f'root.right.left: {aa_tree.root.right.left}')
print(f'root.right.right: {aa_tree.root.right.right}')
print(f'root.right.right.right: {aa_tree.root.right.right.right}')

print(f'root w: {aa_tree.root.weight}')

print(f'\ninordering...')
aa_tree.inorder()








