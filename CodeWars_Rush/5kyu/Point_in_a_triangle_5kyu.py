# accepted on codewars.com
import math
ERR = 10 ** -8


def point_vs_triangle(point: tuple[float, float],
                      triangle: list[list[float, float], list[float, float], list[float, float]]) -> int:
    v1 = [[triangle[2][0], triangle[2][1]], [triangle[0][0], triangle[0][1]]]
    v2 = [[triangle[0][0], triangle[0][1]], [triangle[1][0], triangle[1][1]]]
    v3 = [[triangle[1][0], triangle[1][1]], [triangle[2][0], triangle[2][1]]]
    vectors = [v1, v2, v3]
    v1l, v2l, v3l = distance(v1), distance(v2), distance(v3)
    # the invalid sides:
    if v1l >= v2l + v3l or v2l >= v1l + v3l or v3l >= v1l + v2l:
        raise Exception(f'The triangle is invalid!..')
    # the point is inside the triangle:
    if any(all(point_vs_vector(point, v) == i for v in vectors) for i in [-1, 1]):
        return 1
    # the point is outside the triangle:
    list_ = [point_vs_vector(point, v) for v in vectors]
    if min(list_) < 0 < max(list_):
        return -1
    # the point is on the side
    return 0


def distance(vector):
    return math.hypot(vector[1][0] - vector[0][0], vector[1][1] - vector[0][1])


def point_vs_vector(point: tuple[float, float], vector: list[list[float]]):
    cross_prod = cross_vector_product(vector[0][0] - point[0], vector[0][1] - point[1], vector[1][0] - vector[0][0],
                                      vector[1][1] - vector[0][1])
    if cross_prod > ERR:
        res = -1
    elif cross_prod < -ERR:
        res = 1
    else:
        res = 0
    return res


def cross_vector_product(x1: float, y1: float, x2: float, y2: float) -> float:
    return x1 * y2 - x2 * y1


point_1, triangle_1 = (3, 1), [[0, 0], [5, 5], [5, 0]]
point_2, triangle_2 = (6, 6), [[0, 0], [5, 5], [5, 0]]
point_3, triangle_3 = (2, 0), [[0, 0], [5, 5], [5, 0]]

print(f'res: {point_vs_triangle(point_1, triangle_1)}')
print(f'res: {point_vs_triangle(point_2, triangle_2)}')
print(f'res: {point_vs_triangle(point_3, triangle_3)}')

m = map(lambda x: x ** 2, [1, 2, 3])
print(f'm: {list(m)}')
