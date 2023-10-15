# accepted on codewars.com
from collections import deque
from Node import Node


def tree_by_levels(node):

    deque_of_cases = deque()
    deque_of_cases.append(node)

    result = []

    # bfs...
    while len(deque_of_cases) > 0:
        curr_case = deque_of_cases.pop()

        if curr_case is not None:
            result.append(curr_case.value)

            deque_of_cases.appendleft(curr_case.left)
            deque_of_cases.appendleft(curr_case.right)

    return result


print(tree_by_levels(Node(Node(None, Node(None, None, 4), 2), Node(Node(None, None, 5), Node(None, None, 6), 3), 1)))

