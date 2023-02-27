import time

import arcade


# screen sizes:
SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1050


class W(arcade.Window):

    def __init__(self, width, height):
        super().__init__(width, height)
        arcade.set_background_color(arcade.color.DUTCH_WHITE)
        self.width = width
        self.height = height

    def on_draw(self):
        arcade.start_render()
        arcade.draw_rectangle_outline(100, 500, 100, 100, arcade.color.BLACK)
        sprite = arcade.Sprite('arrow.png')
        sprite.center_x = 800
        sprite.center_y = 290
        sprite.scale = 1 / 16
        sprite.draw()

    def setup(self):
        sprites = arcade.SpriteList()
        start = time.time_ns()
        for i in range(20500):
            # a = i * i + i + 5
            # _h, h, h_ = a / 3, a / 4, a / 5
            # shape = arcade.create_triangles_filled_with_colors(
            #     [
            #         (_h, h),
            #         (h, h_),
            #         (h_, _h)
            #     ],
            #     [
            #         arcade.color.BLACK,
            #         arcade.color.BLACK,
            #         arcade.color.BLACK
            #     ]
            # )
            # sprite = arcade.SpriteCircle(100, arcade.color.BLACK)
            sprite = arcade.Sprite('arrow.png')
            sprites.append(sprite)
        finish = time.time_ns()

        print(f'time elapsed: {(finish - start) // 10 ** 6} milliseconds')

    def update(self, delta_time: float):
        ...


def main():
    # line_width par should be even number for correct grid&nodes representation:
    game = W(SCREEN_WIDTH, SCREEN_HEIGHT)
    game.setup()
    arcade.run()


# start:
if __name__ == "__main__":
    main()
