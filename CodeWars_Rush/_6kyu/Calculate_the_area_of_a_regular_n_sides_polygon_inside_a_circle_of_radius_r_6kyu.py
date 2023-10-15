# accepted on codewars.com
import math


def area_of_polygon_inside_circle(r: int | float, n: int) -> float:
    return round(n * r ** 2 * math.sin(2 * math.pi / n) / 2, 3)


print(f'area: {area_of_polygon_inside_circle(5.8, 7)}')


