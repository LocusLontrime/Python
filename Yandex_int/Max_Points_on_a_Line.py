from collections import defaultdict as d
import math


def max_points(points: list[list[int]]) -> int:
    max_points_on_line = 0
    for j in range(len(points) - 1):
        _x, _y = points[j]
        angles = d(int)
        for i in range(j + 1, len(points)):
            x_, y_ = points[i]
            tan_ = (y_ - _y) / (x_ - _x) if x_ != _x else math.inf
            angles[tan_] += 1
        max_points_on_line = max(max_points_on_line, max(angles.values()))
    return max_points_on_line + 1  # adding the point itself


points_ = [[1, 1], [3, 2], [5, 3], [4, 1], [2, 3], [1, 4]]  # 4

print(f'res: {max_points(points_)}')

