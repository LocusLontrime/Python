import heapq as hq
from enum import Enum

import arcade


# l = [1, 2, 3, 6, 98]
#
# hq.heapify(l)
#
# l.pop()
# l.pop()
# l.pop()
# l.pop()
# l.pop()
#
# print(f'l: {l}')
#
# l.pop()


class NodeType(Enum):
    EMPTY = None
    WALL = arcade.color.BLACK
    VISITED_NODE = arcade.color.ROSE_QUARTZ
    NEIGH = arcade.color.BLUEBERRY
    CURRENT_NODE = arcade.color.ROSE
    START_NODE = arcade.color.GREEN
    END_NODE = (75, 150, 0)
    PATH_NODE = arcade.color.RED


print(f'NodeType(EMPTY): {NodeType.EMPTY.value}')
print(f'NodeType(EMPTY): {NodeType.WALL.value}')

