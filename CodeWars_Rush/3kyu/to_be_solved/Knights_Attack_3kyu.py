import heapq
from typing import Generator, Any

import numpy as np


def attack(start, dest, obstacles):
    # rock your socks off
    pass


def get_pars(field: str) -> tuple[tuple[int, int], tuple[int, int], tuple[tuple[int, int], ...]]:
    start, end, obstacles = None, None, []
    for j, row in enumerate(field.split('\n')):
        for i, el in enumerate(row):
            p = (j, i)
            if el == '*':
                obstacles.append(p)
            elif el == 'S':
                start = p
            elif el == 'E':
                end = p
    if None in [start, end]:
        raise ValueError(f'There is no start or end point!..')
    return start, end, tuple(obstacles)


# represents an infinite board for Knight's attack! game:
class Board:
    def __init__(self, start: tuple[int, int], dest: tuple[int, int], obstacles: tuple[tuple[int, int], ...]):
        # dictionary of all nodes created:
        self.board = dict()
        self.board_inverse = dict()
        # start and end nodes:
        self.start = None
        self.end = None
        self.start_inverse = None
        self.end_inverse = None
        # initialization:
        self.initialize(start, dest, obstacles)
        # a-star priority queue:
        self.vertexes_to_be_visited = None  # straight
        self.vertexes_to_be_visited_inverse = None  # inverse

    def initialize(self, start, dest, obstacles):
        self.start = Node(*start)
        self.board[start] = self.start
        self.start_inverse = Node(*dest)
        self.board_inverse[dest] = self.start_inverse
        self.end = Node(*dest)
        self.board[dest] = self.end
        self.end_inverse = Node(*start)
        self.board_inverse[start] = self.end_inverse
        for obstacle in obstacles:
            self.board[obstacle] = Node(*obstacle, False)
            self.board_inverse[obstacle] = Node(*obstacle, False)

    def gen_neighs(self, node: 'Node', inverse: bool = False) -> Generator['Node', None, Any]:
        nums = [-2, -1, 1, 2]
        _y, _x = node.y, node.x
        coords = [(_y + dy, _x + dx) for dy in nums for dx in nums if abs(dy) != abs(dx)]
        board = self.board_inverse if inverse else self.board
        for y_, x_ in coords:
            if (y_, x_) in board.keys():
                if board[(y_, x_)].passable:
                    yield board[(y_, x_)]
            else:
                board[(y_, x_)] = Node(y_, x_)
                yield board[(y_, x_)]

    def heuristic(self, node_):
        """Manhattan distance..."""
        return abs(node_.y - self.end.y) + abs(node_.x - self.end.x)

    def a_star(self):
        """A-star algorithm for the real time extending graph"""
        # defines important start pars:
        self.vertexes_to_be_visited = [self.start]
        self.vertexes_to_be_visited_inverse = [self.start_inverse]
        self.start.g = 0
        self.start_inverse.g = 0
        # heapifying nodes' list:
        heapq.heapify(self.vertexes_to_be_visited)
        heapq.heapify(self.vertexes_to_be_visited_inverse)
        # the core cycle:
        flag: bool
        while True:
            # forward stroke:
            if len(self.vertexes_to_be_visited) == 0 or self.a_star_step_up():
                flag = False
                print(f'forward stroke EXIT...')
                break
            # return stroke:
            if len(self.vertexes_to_be_visited_inverse) == 0 or self.a_star_step_up(True):
                flag = True
                print(f'return stroke EXIT...')
                break
        # returns the path recovered:
        return self.recover_path(flag)

    def a_star_step_up(self, inverse: bool = False) -> bool:
        curr_node = heapq.heappop(self.vertexes_to_be_visited_inverse if inverse else self.vertexes_to_be_visited)
        # stop condition, here we reach the ending point
        if curr_node == (self.end_inverse if inverse else self.end):
            return True
        # here we're looking for all the adjacent and passable nodes for a current node and pushing them to the heap (priority queue)
        for next_possible_node in self.gen_neighs(curr_node, inverse):
            if next_possible_node.g > curr_node.g + 1:  # a kind of dynamic programming
                next_possible_node.g = curr_node.g + 1  # every step distance from one node to an adjacent one is equal to 1
                # next_possible_node.h = self.heuristic(next_possible_node)  # heuristic function,
                # # needed for sorting the nodes to be visited in priority order
                next_possible_node.previously_visited_node = curr_node  # constructing the path
                # adding node to the heap:
                heapq.heappush(self.vertexes_to_be_visited_inverse if inverse else self.vertexes_to_be_visited,
                               next_possible_node)
        return False

    def recover_path(self, inverse: bool = False) -> list['Node']:
        # the last point of the path found
        node = self.end_inverse if inverse else self.end
        reversed_shortest_path = []
        # path restoring (here we get the reversed path)
        while node.previously_visited_node:
            reversed_shortest_path.append(node)
            node = node.previously_visited_node
        # finally, we need to append the start node:
        reversed_shortest_path.append(self.start_inverse if inverse else self.start)
        # returning the right shortest path
        return list(reversed(reversed_shortest_path))

    def attack(self):
        path = self.a_star()
        print(f'the path: ')
        for path_node in path:
            print(f'{path_node}')
        print(f"the path's length: {(l := len(path))}")
        print(f'forward dict size: {len(self.board)}')
        print(f'return dict size: {len(self.board_inverse)}')
        return l - 1 if l > 1 else None


# class, describing the node's signature:
class Node:
    def __init__(self, y, x, passability=True):
        self.y, self.x = y, x  # (2,5)
        self.passable = passability  # says if a cell is a wall or a path
        self.previously_visited_node = None  # for building the shortest path of Nodes from the starting point to the ending one

        self.g = np.Infinity  # aggregated cost of moving from start to the current Node, Infinity chosen for convenience and algorithm's logic
        self.h = 0  # approximated cost evaluated by heuristic for path starting from the current node and ending at the exit Node
        # f = h + g or total cost of the current Node is not needed here
        ...

    def __eq__(self, other):
        return (self.y, self.x) == (other.y, other.x)

    # this is needed for using Node objects in priority queue like heapq and so on
    def __lt__(self, other):
        return self.h + self.g < other.h + other.g  # the right sigh is "-" for __lt__() method

    def __hash__(self):
        return hash((self.y, self.x))

    def __str__(self):
        return f'({self.y, self.x})[{"_" if self.passable else "W"}]'


# print(f'walk: {list(gen_neighs(98, 989))}')

s = '''\
***********************************************
***********************************************
**  **      **                               **
**  **      **                               **
**  **  **  **  ***************************  **
**  **  **  **  ***************************  **
**  **  **  **  ***      **      **      **  **
**      **      ***  **  **      **      **  **
**   S  **      ***  **  **  **  **  **  **  **
*******************  **  **  **  **  **  **  **
*******************  **  **  **  **  **  **  **
*******************  **  **  **  **  **  **  **
**               **  **  **  **  **  **  **  **
**           E   **  **  **  **  **  **  **  **
**               **  **  **  **  **  **  **  **
**************** **  **  **  **  **  **  **  **
**************** **  **  **  **  **  **  **  **
**               **  **  **  **  **  **  **  **
**               **  **  **  **  **  **  **  **
**               **  **  **  **  **  **  **  **
** ****************  **  **  **  **  **  **  **
** ****************  **  **  **  **  **  **  **
**                   **      **      **  **  **
**                   **      **      **  **  **
**                   **      **      **      **
***********************************************
***********************************************'''  # 105

s_ = '''\
S    
    E
'''  # 3

s__ = '''\
*************************
*   *                   *
*   *                   *
* S *   *****************
*   *   *     * *       *
*********     * *       *
*       *     *E*       *
*       *     * *       *
*************************'''  # 8

s_unreachable = '''\
***************************************************************
***************************************************************
**  S                                                        **
**                                                     E     **
***************************************************************
***************************************************************'''

s_unreachable_z = '''\
S                                      
                    
                    
                    
      * *           
     *   *          
       E            
     *   *          
      * *           
                    
                    
                    
'''

b = Board(*(pars := get_pars(s)))
print(f'pars: {pars}')
print(f'res: {b.attack()}')
