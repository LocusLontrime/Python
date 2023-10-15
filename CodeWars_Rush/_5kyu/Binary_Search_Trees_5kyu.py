# accepted on codewars.com
class Tree(object):
    def __init__(self, root, left=None, right=None):
        assert root and type(root) == Node
        if left:
            assert type(left) == Tree and left.root < root
        if right:
            assert type(right) == Tree and root < right.root

        self.left = left
        self.root = root
        self.right = right

    def is_leaf(self):
        return not (self.left or self.right)

    def __str__(self):

        flag = self.left is None and self.right is None

        if flag:
            left_str = ''
            right_str = ''
        else:
            left_str = '_' if self.left is None else str(self.left)
            right_str = '_' if self.right is None else str(self.right)

        core = str(self.root)

        gap = '' if flag else ' '

        return f'[{left_str}{gap}{core}{gap}{right_str}]'

    def __eq__(self, other):

        if self.root != other.root:
            return False

        if (self.left is not None and other.left is None) or (self.left is None and other.left is not None):
            return False

        if (self.right is not None and other.right is None) or (self.right is None and other.right is not None):
            return False

        if self.left != other.left or self.right != other.right:
            return False

        return True

    def __ne__(self, other):
        return not self == other


class Node(object):

    def __init__(self, value, weight=1):
        self.value = value
        self.weight = weight

    def __str__(self):
        return str(self.value)

    def __lt__(self, other):
        return self.value < other.value

    def __gt__(self, other):
        return self.value > other.value

    def __eq__(self, other):
        return self.value == other.value

    def __ne__(self, other):
        return self.value != other.value


tree1 = Tree(Node('B'), Tree(Node('A')), Tree(Node('C')))
tree2 = Tree(Node('F'), Tree(Node('E')), Tree(Node('G')))
tree3 = Tree(Node('D'), tree1, tree2)

print(str(tree1))
print(str(tree2))
print(str(tree3))

tree1 = Tree(Node('B'), None, Tree(Node('C')))
tree2 = Tree(Node('B'), None, Tree(Node('C')))

print(tree1 == tree2)

tree1 = Tree(Node('B'), Tree(Node('A')), Tree(Node('C')))
tree2 = Tree(Node('B'), None, Tree(Node('C')))

print(tree1 != tree2)








































