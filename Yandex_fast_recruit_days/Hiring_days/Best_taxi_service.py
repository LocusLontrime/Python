import math


def best_service(r: int, t: int, n: int, m: int, taxis1: tuple[tuple[int, int], ...],
                 taxis2: tuple[tuple[int, int], ...]) -> str:
    result, counter = '', 0
    valid_taxis1, valid_taxis2 = [], []
    # taxis1 validation:
    sd1, sd2 = math.inf, math.inf
    for taxi1 in taxis1:
        if (sd := shortest_distance(taxi1, r)) <= t:
            sd1 = min(sd1, sd)
            valid_taxis1.append((taxi1, sd))
    # taxis2 validation:
    for taxi2 in taxis2:
        if (sd := shortest_distance(taxi2, r)) <= t:
            sd2 = min(sd2, sd)
            valid_taxis2.append((taxi2, sd))
    if sd1 < sd2:
        for _, sd in valid_taxis1:
            if sd < sd2:
                counter += 1
        result = f'1\n{counter}'
    elif sd1 > sd2:
        for _, sd in valid_taxis2:
            if sd < sd1:
                counter += 1
        result = f'2\n{counter}'
    else:
        result = '0\n0'
    return result


def shortest_distance(point: tuple[int, int], r: int) -> float:
    # checks if the point of the projection of the center of the circle on straight line p1p2 lies into the segment p1p2...
    # orthogonal straight line to p1p2, let it be named as "orto",
    # circle's center belongs to the orto straight line, consequently:
    a, b, c, (x1, y1), (x2, y2) = get_coeffs(r, point)
    c_ = a * point[1] - b * point[0]
    # aux par:
    h = a ** 2 + b ** 2
    # now let us define the coordinates of projection point:
    x_, y_ = (-b * c_ - a * c) / h, (a * c_ - b * c) / h
    # segment check:
    if min(x1, x2) <= x_ <= max(x1, x2) and min(y1, y2) <= y_ <= max(y1, y2):
        res = point_to_straight_line_distance(point, a, b, c) * math.sqrt(2)
    else:
        res = min(manhattan_distance((x1, y1), (x_, y_)), manhattan_distance((x2, y2), (x_, y_)))
    return res


def manhattan_distance(p1: tuple[int, int], p2: tuple[int, int]) -> float:
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])


def point_to_straight_line_distance(point: tuple[int, int], a: int, b: int, c: int) -> float:
    return (a * point[0] + b * point[1] + c) / math.hypot(a, b)


def get_coeffs(r: int, taxi_coords: tuple[int, int]):
    x, y = taxi_coords
    return x // abs(x), y // abs(y), r, (r * x // abs(x), 0), (0, r * y // abs(y))
