# accepted on leetcode.com

from collections import deque as deq

walk = ((1, 0), (0, -1), (-1, 0), (0, 1))


def cut_off_tree(forest: list[list[int]]) -> int:
    # linear sizes:
    max_j, max_i = len(forest), len(forest[0])
    # let us sort all the trees in the ascending order:
    trees = []
    for j in range(max_j):
        for i in range(max_i):
            if (tree := forest[j][i]) > 1:
                trees += [(tree, j, i)]
    print(f'{trees = }')
    trees.sort(key=lambda x: x[0])
    print(f'sorted {trees = }')
    path = 0
    j_, i_ = 0, 0
    for ind, (tree, jt, it) in enumerate(trees):
        print(f'{ind} -> trying to cut tree [{tree}] at {jt, it = }')
        visited = set()
        r = bfs(j_, i_, max_j, max_i, tree, forest, visited)
        if r == -1:
            path = -1
            break
        path += r
        print(f'...{path = }')
        # cutting the tree:
        forest[jt][it] = 1
        # new coords:
        j_, i_ = jt, it
        print_forest(forest)
    return path


def bfs(j_start: int, i_start: int, max_j: int, max_i: int, tree: int, forest: list[list[int]], visited: set) -> int:
    # starting point (j, i) is added to deque:
    nodes_to_be_visited = deq([(j_start, i_start, 0)])
    path = 0
    while nodes_to_be_visited:
        # popping out the leftmose node:
        j, i, path = nodes_to_be_visited.popleft()
        # checks reaching the tree:
        if forest[j][i] == tree:
            # the tree to be cutted found:
            return path
        # getting vh neighs:
        for dj, di in walk:
            j_, i_ = j + dj, i + di
            # we should stay within the borders:
            if 0 <= j_ < max_j and 0 <= i_ < max_i:
                # the node needed to not be visited:
                if (j_, i_) not in visited:
                    # the cell is empty (1) or contains the (tree) needed:
                    if forest[j_][i_]:  # tree-nodes are walkthroughable;)
                        # visiting the node:
                        visited |= {(j_, i_)}
                        # appending it to the deque to the right:
                        nodes_to_be_visited += [(j_, i_, path + 1)]
    # returns -1 if the tree cannot be reached:
    return -1


def print_forest(forest: list[list[int]]):
    for row in forest:
        print(f'{row}')


test_ex = [
    [1, 2, 3],
    [0, 0, 4],
    [7, 6, 5]
]

test_ex_1 = [
    [1, 2, 3],
    [0, 0, 0],
    [7, 6, 5]
]

test_ex_2 = [
    [2, 3, 4],
    [0, 0, 5],
    [8, 7, 6]
]

test_ex_err = [
    [8, 11, 4, 13],
    [16, 10, 12, 14],
    [1, 19, 18, 20],
    [15, 3, 6, 7],
    [17, 2, 5, 9]
]

print(f'test ex res -> {cut_off_tree(test_ex)}')                                      # 36 366 98 989 98989 LL LL
print(f'test ex 1 res -> {cut_off_tree(test_ex_1)}')
print(f'test ex 2 res -> {cut_off_tree(test_ex_2)}')
print(f'test ex err res -> {cut_off_tree(test_ex_err)}')


