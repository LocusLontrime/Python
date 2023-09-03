# accepted on codewars
DIRS = ((-1, 0), (0, 1), (1, 0), (0, -1))
AUX_DIRS = ((-1, 1), (1, 1), (1, -1), (-1, -1))


class Image:  # 36.6 98 989 LL
    def __init__(self, data: list[int], w: int, h: int):
        self.pixels = data
        self.width = w
        self.height = h


class CentralPixelsFinder(Image):

    def num(self, y: int, x: int):
        return y * self.width + x

    def touch_border(self, y: int, x: int, pixels: list[list[int]], colour: int) -> bool:
        for dir_ in DIRS:
            y_, x_ = y + dir_[0], x + dir_[1]
            if not self.is_valid(y_, x_) or pixels[y_][x_] != colour:
                return True
        return False

    def is_valid(self, y: int, x: int):
        return 0 <= y < self.height and 0 <= x < self.width

    def central_pixels(self, colour: int):
        pixels: list[list[int]] = [[colour for _, colour in enumerate(self.pixels[y * self.width: (y + 1) * self.width])] for y in range(self.height)]
        visited: list[list[bool]] = [[False for _ in range(self.width)] for _ in range(self.height)]
        pixel_layer = set()
        deepest_depth = 0
        deepest_pixels = []
        # main cycle through the pixels:
        colour_domain_counter = 0
        for y in range(self.height):
            for x in range(self.width):
                if not visited[y][x] and pixels[y][x] == colour:
                    colour_domain_counter += 1
                    # border building:
                    queue = [(y, x)]
                    while queue:
                        _y, _x = queue.pop()
                        if self.is_valid(_y, _x) and not visited[_y][_x] and pixels[_y][_x] == colour and self.touch_border(_y, _x, pixels, colour):
                            visited[_y][_x] = True
                            pixel_layer.add((_y, _x))
                            for dir_ in DIRS + AUX_DIRS:
                                y_, x_ = _y + dir_[0], _x + dir_[1]
                                queue.append((y_, x_))
                    # iterative deepening:
                    next_layer = set()
                    iteration = 1
                    while True:
                        for _y, _x in pixel_layer:
                            for dir_ in DIRS:
                                y_, x_ = _y + dir_[0], _x + dir_[1]
                                if self.is_valid(y_, x_) and not visited[y_][x_] and pixels[y_][x_] == colour and (y_, x_) not in pixel_layer:
                                    visited[y_][x_] = True
                                    next_layer.add((y_, x_))
                        if not next_layer:
                            break
                        iteration += 1
                        pixel_layer = next_layer
                        next_layer = set()
                    nums = [self.num(y_, x_) for y_, x_ in pixel_layer]
                    if iteration > deepest_depth:
                        deepest_depth = iteration
                        deepest_pixels = nums
                    elif iteration == deepest_depth:
                        deepest_pixels += nums
        return deepest_pixels


image_x = CentralPixelsFinder(
    [
        1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
        1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1,
        1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1,
        1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1,
        1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1,
        1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1,
        1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1,
        1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1,
        1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1,
        1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1,
        1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1,
        1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1,
        1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1,
        1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1,
        1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1,
        1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1,
        1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1,
        1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1
    ],
    16 + 2,
    16 + 2
)

image = CentralPixelsFinder(
    [
        1, 1, 4, 4, 4, 4, 2, 2, 2, 2,
        1, 1, 1, 1, 2, 2, 2, 2, 2, 2,
        1, 1, 1, 1, 2, 2, 2, 2, 2, 2,
        1, 1, 1, 1, 1, 3, 2, 2, 2, 2,
        1, 1, 1, 1, 1, 3, 3, 3, 2, 2,
        1, 1, 1, 1, 1, 1, 3, 3, 3, 3
    ],
    10,
    6
)

image_y = CentralPixelsFinder(
    [
        57, 57, 57, 57, 57,
        56, 57, 57, 57, 57,
        56, 56, 57, 57, 57,
        56, 56, 56, 57, 57,
        56, 56, 56, 56, 57
    ],
    5,
    5
)

image_xxx = CentralPixelsFinder(
    [
        7, 7, 7, 7, 7, 5, 5, 5, 6, 6, 6, 6, 6, 6, 6, 5, 5, 5, 5, 5, 7, 7, 7, 7, 7, 5, 5, 5, 7,
        5, 5, 5, 5, 5, 5, 5, 5, 7, 7, 7, 7, 7, 6, 6, 7, 7, 7, 7, 7, 6, 6, 5, 5, 5, 7, 7, 7, 7,
        5, 5, 5, 5, 5, 5, 5, 5, 7, 7, 7, 7, 7, 6, 6, 7, 7, 7, 7, 7, 6, 6, 5, 5, 5, 7, 7, 7, 7,
        5, 5, 5, 5, 5, 5, 5, 5, 7, 7, 7, 7, 7, 6, 6, 7, 7, 7, 7, 7, 6, 6, 5, 5, 5, 7, 7, 7, 7,
        5, 5, 5, 5, 5, 5, 5, 5, 7, 7, 7, 7, 7, 6, 6, 7, 7, 7, 7, 7, 6, 6, 5, 5, 5, 7, 7, 7, 7,
        5, 5, 5, 5, 5, 5, 5, 5, 7, 7, 7, 7, 7, 6, 6, 7, 7, 7, 7, 7, 6, 6, 5, 5, 5, 7, 7, 7, 7,
        6, 6, 6, 6, 7, 6, 6, 5, 5, 5, 7, 7, 7, 7, 7, 5, 5, 5, 5, 5, 5, 5, 7, 7, 7, 6, 6, 6, 5,
        6, 6, 6, 6, 7, 6, 6, 5, 5, 5, 7, 7, 7, 7, 7, 5, 5, 5, 5, 5, 5, 5, 7, 7, 7, 6, 6, 6, 5,
        5, 5, 5, 5, 7, 6, 6, 6, 6, 6, 6, 6, 6, 7, 7, 5, 5, 5, 5, 5, 5, 5, 7, 7, 7, 5, 5, 5, 7,
        5, 5, 5, 5, 7, 6, 6, 6, 6, 6, 6, 6, 6, 7, 7, 5, 5, 5, 5, 5, 5, 5, 7, 7, 7, 5, 5, 5, 7,
        5, 5, 5, 5, 5, 6, 6, 6, 6, 6, 5, 5, 5, 7, 7, 6, 6, 6, 6, 6, 5, 5, 7, 7, 7, 6, 6, 6, 7,
        5, 5, 5, 5, 5, 6, 6, 6, 6, 6, 5, 5, 5, 7, 7, 6, 6, 6, 6, 6, 5, 5, 7, 7, 7, 6, 6, 6, 7,
        5, 5, 5, 5, 5, 6, 6, 6, 6, 6, 5, 5, 5, 7, 7, 6, 6, 6, 6, 6, 5, 5, 7, 7, 7, 6, 6, 6, 7,
        5, 5, 5, 5, 5, 6, 6, 6, 6, 6, 5, 5, 5, 7, 7, 6, 6, 6, 6, 6, 5, 5, 7, 7, 7, 6, 6, 6, 7,
        5, 5, 5, 5, 5, 6, 6, 6, 6, 6, 5, 5, 5, 7, 7, 6, 6, 6, 6, 6, 5, 5, 7, 7, 7, 6, 6, 6, 7,
        7, 7, 7, 7, 7, 5, 5, 6, 5, 5, 6, 6, 6, 7, 7, 6, 6, 6, 6, 6, 5, 5, 5, 5, 5, 6, 6, 6, 7,
        7, 7, 7, 7, 7, 5, 5, 6, 5, 5, 6, 6, 6, 7, 7, 6, 6, 6, 6, 6, 5, 5, 5, 5, 5, 6, 6, 6, 7,
        7, 7, 7, 7, 7, 5, 5, 6, 5, 5, 6, 6, 6, 7, 7, 6, 6, 6, 6, 6, 5, 5, 5, 5, 5, 6, 6, 6, 7,
        5, 5, 5, 5, 7, 7, 7, 7, 7, 7, 6, 6, 6, 7, 7, 6, 6, 6, 6, 6, 5, 5, 7, 7, 7, 5, 5, 5, 7,
        5, 5, 5, 5, 7, 7, 7, 7, 7, 7, 6, 6, 6, 7, 7, 6, 6, 6, 6, 6, 5, 5, 7, 7, 7, 5, 5, 5, 7,
        6, 6, 6, 6, 5, 6, 6, 6, 6, 6, 6, 6, 6, 7, 7, 5, 5, 5, 5, 5, 5, 5, 7, 7, 7, 7, 7, 7, 6,
        6, 6, 6, 6, 5, 6, 6, 6, 6, 6, 6, 6, 6, 7, 7, 5, 5, 5, 5, 5, 5, 5, 7, 7, 7, 7, 7, 7, 6,
        6, 6, 6, 6, 5, 6, 6, 6, 6, 6, 6, 6, 6, 7, 7, 5, 5, 5, 5, 5, 5, 5, 7, 7, 7, 7, 7, 7, 6,
        5, 5, 5, 5, 6, 7, 7, 5, 7, 7, 5, 5, 5, 5, 5, 6, 6, 6, 6, 6, 5, 5, 6, 6, 6, 6, 6, 6, 5,
        7, 7, 7, 7, 7, 6, 6, 7, 6, 6, 7, 7, 7, 5, 5, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 5, 5, 5, 7,
        7, 7, 7, 7, 7, 6, 6, 7, 6, 6, 7, 7, 7, 5, 5, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 5, 5, 5, 7,
        7, 7, 7, 7, 7, 6, 6, 7, 6, 6, 7, 7, 7, 5, 5, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 5, 5, 5, 7,
        7, 7, 7, 7, 7, 6, 6, 7, 6, 6, 7, 7, 7, 5, 5, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 5, 5, 5, 7,
        7, 7, 7, 7, 7, 6, 6, 7, 6, 6, 7, 7, 7, 5, 5, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 5, 5, 5, 7
    ],
    29,
    29
)

res = image.central_pixels(2)
print(f'res: {res}')

# a = {2, 3}
# b = {4, 5}
#
# a = b
# b = {}
#
# print(f'a, b: {a, b}')
