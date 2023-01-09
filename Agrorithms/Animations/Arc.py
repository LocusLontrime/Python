import arcade


# screen sizes:
SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1050
TILE_SIZE: int


# opening a new window with following parameters:
t = arcade.open_window(SCREEN_WIDTH, SCREEN_HEIGHT, "Game")
# defining a back color:
arcade.set_background_color(arcade.color.WHITE_SMOKE)
# starting rendering, it should be done before drawing:
arcade.start_render()
# The drawing has begun:
# arcade.draw_line(500, 500, 1450, 500, arcade.color.BLACK, 5)
for i in range(16):
    arcade.draw_rectangle_filled(98 + i * 100, 500, 98, 98, (255 - 5 * i, 5 * i, 127 - 5 * i))
# Finishing rendering and showing the result:
arcade.finish_render()

# runs a window until 'Escape' button is pressed:
arcade.run()


print(f'{arcade.color.ROSE}')