import math

import arcade
# screen sizes:
SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080

# opening a new window with following parameters:
arcade.open_window(SCREEN_WIDTH, SCREEN_HEIGHT, "Game")
# defining a back color:
arcade.set_background_color(arcade.color.WHITE_SMOKE)
# starting rendering, it should be done before drawing:
arcade.start_render()
# The drawing has begun:
# arcade.draw_line(500, 500, 1450, 500, arcade.color.BLACK, 5)


# recursive drawing magic:
def draw_inclined_line(starting_x, starting_y, line_length, line_width, prev_angle):
    new_angle = prev_angle
    cos_rotation_angle, sin_rotation_angle = math.cos(new_angle), math.sin(new_angle)
    # print(f'sin: {sin_rotation_angle}, cos: {cos_rotation_angle}')
    new_x, new_y = starting_x + line_length * sin_rotation_angle, starting_y + line_length * cos_rotation_angle
    # print(f'new_x: {new_x}, new_y: {new_y}')
    arcade.draw_line(starting_x, starting_y, new_x, new_y, arcade.color.BLACK, line_width)
    return new_x, new_y


def rec_tree_builder(starting_x, starting_y, line_length, line_width, prev_angle, delta_angle):
    if line_length >= 8:
        k = 1.5
        new_x, new_y = draw_inclined_line(starting_x, starting_y, line_length, line_width, prev_angle)
        rec_tree_builder(new_x, new_y, line_length // k, line_width, prev_angle + delta_angle, delta_angle)
        rec_tree_builder(new_x, new_y, line_length // k, line_width, prev_angle - delta_angle, delta_angle)
        if line_length < 128:
            rec_tree_builder(new_x, new_y, line_length // k, line_width, prev_angle + 2 * delta_angle, delta_angle)
            rec_tree_builder(new_x, new_y, line_length // k, line_width, prev_angle - 2 * delta_angle, delta_angle)


rec_tree_builder(960, 0, 256, 2, 0, math.pi * 1.5 * 2 * 15 / 180)


# Finishing rendering and showing the result:
arcade.finish_render()
# Until the user press 'Esc' button the window will be opened:
arcade.run()

















































