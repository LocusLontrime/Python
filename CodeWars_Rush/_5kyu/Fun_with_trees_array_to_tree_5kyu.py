# accepted on codewars.com
class Node:
    def __init__(self, value, left=None, right=None):
        self.value = value
        self.left = left
        self.right = right

    def __str__(self):
        return f'{self.value}'

    def __repr__(self):
        return str(self)


def array_to_tree(arr: list[int]):
    if not arr:
        return None
    root = Node(arr[0])
    i = 1
    nodes_queue = [root]
    flag = False if len(arr) == 1 else True
    while flag:
        new_nodes = []
        for node_ in nodes_queue:
            node_.left = Node(arr[i])
            new_nodes.append(node_.left)
            i += 1
            if i == len(arr):
                flag = False
                break
            node_.right = Node(arr[i])
            new_nodes.append(node_.right)
            i += 1
            if i == len(arr):
                flag = False
                break
        nodes_queue = [node for node in new_nodes]
    return root


def dfs(node_: Node):
    return f'{dfs(node_.left)}[{node_}]{dfs(node_.right)}' if node_ else f'_'


arr_ = [17, 0, -4, 3, 15]
arr_x = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]
array_to_tree(arr_)






