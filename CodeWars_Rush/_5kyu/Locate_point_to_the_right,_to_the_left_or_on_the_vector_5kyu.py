# accepted on codewars.com
def point_vs_vector(point: tuple[float, float], vector: list[list[float]]) -> int:
    cross_prod = cross_vector_product(vector[0][0] - point[0], vector[0][1] - point[1], vector[1][0] - vector[0][0], vector[1][1] - vector[0][1])
    if cross_prod > 0:
        res = -1
    elif cross_prod < 0:
        res = 1
    else:
        res = 0
    return res


def cross_vector_product(x1: float, y1: float, x2: float, y2: float) -> float:
    return x1 * y2 - x2 * y1


vector_ = [[0, 0], [1, 1]]
point_1 = 0, 1
point_2 = 2, 2
point_3 = 2, 0


print(f'res: {point_vs_vector(point_1, vector_)}')
print(f'res: {point_vs_vector(point_2, vector_)}')
print(f'res: {point_vs_vector(point_3, vector_)}')

