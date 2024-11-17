# -*- coding: utf-8 -*-

# Дан массив точек с целочисленными координатами (x, y).
# Определить, существует ли вертикальная прямая,
# делящая точки на 2 симметричных относительно этой прямой множества.
#
# Задача повышенной сложности из АА (алгоритмического) собеседования в Яндекс.

def check(points: list[tuple[int, int]]):
    # 1. let us find the x median of set given:
    x_median = get_median_x(points)
    print(f'{x_median = }')

    # 2. now we can check the symmetry of left and right set:
    # 2.1 if the point is on the x = x_median line -> it is symmetric to itself by default:
    points_set: set[tuple[int, int]] = set(point for point in points if point[0] != int(x_median))

    iteration = 0

    while points_set:
        iteration += 1
        # at first gets a random point:
        point_ = points_set.pop()
        print(f'{iteration}. current point -> {point_}')
        # defines a symmetric one:
        symmetric_point_ = (int(2 * x_median - point_[0]), point_[1])
        print(f'{iteration}. symmetric_point_ -> {symmetric_point_}')
        # if this point is NOT in set -> vertical line x = x_median cannot be chosen:
        if symmetric_point_ not in points_set:
            return False
        # if in:
        points_set.remove(symmetric_point_)

    return True


def get_median_x(points: list[tuple[int, int]]) -> float:
    return sum([x for x, y in points]) / len(points)


# some tests:
points_given = [(-5 + 1, 1), (3 + 1, 2), (-98 + 1, 0), (5 + 1, 1), (-3 + 1, 2), (98 + 1, 0)]

points_given_test_1 = [(1, 3), (3, 3), (2, 2), (2, 10), (0, 4), (4, 4)]

wrong_test = [(1, 4), (3, 3), (6, 2)]

print(f'res: {check(wrong_test)}')


















































