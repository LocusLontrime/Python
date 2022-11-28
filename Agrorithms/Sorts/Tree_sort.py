def tree_sort(array: list[int]):

    if len(array) == 0:
        print(f"Array's length cannot be equal to zero!")
        return None
    # the root of BST:
    root = Node(array[0])

    # building a BST:
    for i in range(1, len(array)):
        root.insert(array[i])

    result = []
    get_sorted_data(root, result)

    return result


# recursive building of result sorted array from BST made:
def get_sorted_data(node, result: list[int]):
    if node:
        get_sorted_data(node.left_leaf, result)
        result.append(node.value)
        get_sorted_data(node.right_leaf, result)


# class for the tree's leaf (node):
class Node:
    def __init__(self, value, left_leaf=None, right_leaf=None):
        self.value = value
        self.freq = 1
        self.left_leaf = left_leaf
        self.right_leaf = right_leaf

    def insert(self, value):
        # None-case:
        if self is None:
            return None
        # body of rec and recurrent relation:
        if value == self.value:
            self.freq += 1
        elif value < self.value:
            if self.left_leaf is None:
                # left-side insertion itself:
                self.left_leaf = Node(value)
                return
            # descending:
            self.left_leaf.insert(value)
        else:
            if self.right_leaf is None:
                # right-side insertion itself:
                self.right_leaf = Node(value)
                return
            # descending:
            self.right_leaf.insert(value)

    def __repr__(self):
        return f'{self.value}'

    def __str__(self):
        return f'{self.value}'


# bad testcase:
arr = [111, 1, 7, 17, 7, 0, 0, -166, 1, 68, 178, 98, 111, 1, 98, 989, 98]
print(tree_sort(arr))
