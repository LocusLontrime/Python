import heapq
import math
import random

walk = ((1, 0), (0, -1), (-1, 0), (0, 1))

RED = "\033[31m{}"
END = "\033[0m{}"


def swim_in_water(grid: list[list[int]]) -> int:
    # linear sizes:
    max_j, max_i = len(grid), len(grid[0])
    # initialization of nodes:
    board = [[Node(j, i, grid[j][i]) for i in range(max_i)] for j in range(max_j)]
    # here dijkstra's algorithm starts working:
    nodes_to_be_visited = [board[0][0]]
    board[0][0].g = board[0][0].t  # starting point
    heapq.heapify(nodes_to_be_visited)
    iters = 0
    while nodes_to_be_visited:
        iters += 1
        # the most priority node:
        node_ = heapq.heappop(nodes_to_be_visited)
        # print(f'{node_ = }')
        # check for reaching the exit:
        if (node_.j, node_.i) == (max_j - 1, max_i - 1):
            print(f'{iters} iterations been made...')
            path = recover_path(node_)
            print(f'path -> {path}')
            print_board(board, set(path))
            print(f"path's length: {len(path)}")
            return node_.g
        # process neighs:
        for dj, di in walk:
            j_, i_ = node_.j + dj, node_.i + di
            if 0 <= j_ < max_j and 0 <= i_ < max_i:
                if board[j_][i_].g > node_.g:
                    board[j_][i_].g = max(node_.g, board[j_][i_].t)
                    board[j_][i_].prev = node_
                    heapq.heappush(nodes_to_be_visited, board[j_][i_])


def recover_path(node: 'Node'):
    chain = []
    while node:
        chain += [(node.j, node.i)]
        node = node.prev
    return chain[::-1]


def print_board(board: list[list['Node']], path: set[tuple[int, int]]):
    for j in range(len(board)):
        for i in range(len(board[0])):
            print(f'{colour_(board[j][i], RED) if (j, i) in path else board[j][i]} ', end='')
        print()


class Node:
    def __init__(self, j: int, i: int, t=0):
        self.j = j
        self.i = i
        self.t = t  # min time of reaching this node
        self.g = math.inf  # cost in time of reaching this node (for dijkstra)
        # path connected info:
        self.prev = None

    def __repr__(self):
        return f'{self.g}'

    def __lt__(self, other: 'Node'):
        return self.t < other.t


def colour_(char, colour, flag=False):
    s = "\033[1m" if flag else ''
    return f"{(s + colour).format(char)}{END.format('')}"


test_ex = [                                                                           # 16
    [0, 1, 2, 3, 4],
    [24, 23, 22, 21, 5],
    [12, 13, 14, 15, 16],
    [11, 17, 18, 19, 20],
    [10, 9, 8, 7, 6]
]

n = 29

dicky_tricky_mighty_huuuuuuuuuuuge_ex = [[random.randint(0, n ** 2 - 1) for _ in range(n)] for _ in range(n)]

print(f'test ex res -> {swim_in_water(test_ex)}')                                     # 36 366 98 989 98989 LL LL
print(f'test ex res -> {swim_in_water(dicky_tricky_mighty_huuuuuuuuuuuge_ex)}')
