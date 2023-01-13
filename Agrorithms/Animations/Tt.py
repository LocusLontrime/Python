import heapq as hq
from enum import Enum

import arcade

# class NodeType(Enum):
#     EMPTY = None
#     WALL = arcade.color.BLACK
#     VISITED_NODE = arcade.color.ROSE_QUARTZ
#     NEIGH = arcade.color.BLUEBERRY
#     CURRENT_NODE = arcade.color.ROSE
#     START_NODE = arcade.color.GREEN
#     END_NODE = (75, 150, 0)
#     PATH_NODE = arcade.color.RED
#
#
# print(f'NodeType(EMPTY): {NodeType.EMPTY.value}')
# print(f'NodeType(EMPTY): {NodeType.WALL.value}')
# print(f'{(1, 2, 98) * 98}')


def draw_lock(center_x: int, center_y: int):
    arcade.open_window(1920, 1080, 'Lock')
    arcade.set_background_color(arcade.color.WHITE_SMOKE)
    arcade.start_render()
    arcade.draw_rectangle_filled(center_x, center_y, 14, 14, arcade.color.BLACK)
    arcade.draw_rectangle_outline(center_x, center_y + 7, 8.4, 16.8, arcade.color.BLACK, border_width=2)
    arcade.finish_render()
    arcade.run()


draw_lock(900, 500)

