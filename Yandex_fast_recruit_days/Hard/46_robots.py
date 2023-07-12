import math
import sys
from collections import deque


def min_gathering_time():
    graph, filling, filled_rooms_counter = get_graph()
    min_time = math.inf
    print(f'filled_rooms_counter: {filled_rooms_counter}')
    for i, room_ in enumerate(graph.keys()):
        val = bfs(room_, filled_rooms_counter, graph, filling)
        print(f'{i}. val: {val}')
        if val == -1:
            return val
        min_time = min(min_time, val)
    return min_time


def bfs(start_room: int, max_filled_rooms_counter: int, graph: dict[int, set[int]], filling: dict[int, bool]) -> int:
    # main pars:
    deq = deque()
    deq.append((start_room, 0))
    visited_rooms = set()
    # core cycle:
    while deq:
        # descending_counter += 1
        room_, depth_ = deq.popleft()
        visited_rooms.add(room_)
        if filling[room_]:
            max_filled_rooms_counter -= 1
            print(f'depth_: {depth_}')
            if max_filled_rooms_counter == 0:
                return depth_
        for neighbouring_room in graph[room_]:
            if neighbouring_room not in visited_rooms:
                deq.append((neighbouring_room, depth_ + 1))
    if filling[start_room] and max_filled_rooms_counter > 0:
        return -1
    return 20_000 + 1


def get_graph() -> tuple[dict[int, set[int]], dict[int, bool], int]:
    # splitting pars:
    n, k = [int(_) for _ in input().split(' ') if _.isdigit()]
    # graph skeleton:
    graph: dict[int, set[int]] = {_: set() for _ in range(1, n + 1)}
    # aux dict:
    filling: dict[int, bool] = {_: False for _ in range(1, n + 1)}
    # graph building:
    for _ in range(k):
        r1, r2 = [int(_) for _ in input().split(' ') if _.isdigit()]
        # links:
        if r1 != r2:
            graph[r1].add(r2)
            graph[r2].add(r1)
    # filling rooms with robots:
    input()  # m ???
    filled_rooms = [int(_) for _ in input().split(' ') if _.isdigit()]
    filled_rooms_counter = 0
    for filled_room in filled_rooms:
        if not filling[filled_room]:
            filling[filled_room] = True
            filled_rooms_counter += 1
    return graph, filling, filled_rooms_counter


print(f'min time: {min_gathering_time()}')

# 3 3
# 1 2
# 1 3
# 2 3
# 3
# 1 2 3














# lala                                                                                