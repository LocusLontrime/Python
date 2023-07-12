# accepted on coderun
import random
import sys
import math

vertices = [(0, 0), (0, 1), (1, 1), (1, 0)]


def get_math_exp():
    n, r, points = get_pars()
    math_exp = 0
    for x_, y_ in points:
        math_exp += get_math_exp_1_point(x_, y_, r)
    print(f'{math_exp}')


def get_math_exp_1_point(x_: float, y_: float, r: float):
    # check for circle-in-square placement:
    if min(1 - x_, x_, 1 - y_, y_) >= r:
        alpha = math.pi * r ** 2
        return alpha
    # let us find the distances from the point to all the square's vertices:
    ld, lu, ru, rd = (math.hypot(vx_ - x_, vy_ - y_) for vx_, vy_ in vertices)
    # check for square-in-circle placement:
    if max(ld, lu, ru, rd) <= r:
        return 1.0
    # number of square's vertices that located inside the circle:
    vertices_in_ = [i for i, _ in enumerate([ld, lu, ru, rd]) if _ <= r]
    vertices_out_ = [i for i in range(4) if i not in vertices_in_]
    vertices_in = sum(1 for _ in [ld, lu, ru, rd] if _ <= r)
    # computing the points of intersections for all the square's sides and the circle:
    points_on_sides = get_points_of_intersection(r, x_, y_)
    points_segments_on_sides = sum(1 for p in points_on_sides.values() if len(p) == 2)
    points_segments_on_sides_ = [i for i in range(4) if len(points_on_sides[i]) == 2]
    # cases processing:
    # 1. no vertices in:
    if vertices_in == 0:
        # area of the circle without all the outer segments:
        return circle_area(r) - sum(segment_area(r, x_, y_, *p) for p in points_on_sides.values() if len(p) == 2)
    # 2. 1 vertices in:
    if vertices_in == 1:
        v_in_ind = vertices_in_[0]
        vertex_in = vertices[v_in_ind]
        # 2.1 sub-case -->> 0 segments out:
        if points_segments_on_sides == 0:
            # triangle and segment areas:
            points = get_corner_points(v_in_ind, points_on_sides)
            return segment_area(r, x_, y_, *points) + area_heron(vertex_in, *points)
        # 2.2 sub-case -->> 1 segments out:
        elif points_segments_on_sides == 1:
            segment_on_side = points_segments_on_sides_[0]
            if (segment_on_side + 2) % 4 == v_in_ind:
                v_corner_ind = (v_in_ind + 3) % 4
                p1, p2 = points_on_sides[segment_on_side][0], points_on_sides[v_in_ind][0]
            else:
                v_corner_ind = (v_in_ind + 1) % 4
                p2, p1 = points_on_sides[(v_in_ind + 3) % 4][0], points_on_sides[v_corner_ind][1]
            points = get_corner_points(v_corner_ind, points_on_sides)
            corner_point = vertices[v_corner_ind]
            return segment_area(r, x_, y_, p1, p2) + trapeze_area(
                math.hypot(
                    p1[0] - corner_point[0],
                    p1[1] - corner_point[1]
                ),
                math.hypot(
                    p2[0] - vertex_in[0],
                    p2[1] - vertex_in[1]
                ),
                1) - corner_area(r, x_, y_, *points, corner_point)
        # 2.3 sub-case --> 2 segments out:
        else:
            return 1 - corner_area(
                r, x_, y_, *get_corner_points(vertices_out_[0], points_on_sides), vertices[vertices_out_[0]]
            ) - corner_area(
                r, x_, y_, *get_corner_points(vertices_out_[1], points_on_sides), vertices[vertices_out_[1]]
            ) - corner_area(
                r, x_, y_, *get_corner_points(vertices_out_[2], points_on_sides), vertices[vertices_out_[2]]
            )
    # 3. 2 vertices in:
    if vertices_in == 2:
        # 3.1 sub-case -->> 0 segments out:
        if points_segments_on_sides == 0:
            left, right = lr(*vertices_in_)
            p1, p2 = points_on_sides[(left + 3) % 4][0], points_on_sides[right][0]
            return trapeze_area(
                math.hypot(p1[0] - vertices[left][0], p1[1] - vertices[left][1]),
                math.hypot(p2[0] - vertices[right][0], p2[1] - vertices[right][1]),
                1
            ) + segment_area(r, x_, y_, p1, p2)
        # 3.2 sub-case -->> 1 segments out:
        else:
            return 1 - corner_area(
                r, x_, y_, *get_corner_points(vertices_out_[0], points_on_sides), vertices[vertices_out_[0]]
            ) - corner_area(
                r, x_, y_, *get_corner_points(vertices_out_[1], points_on_sides), vertices[vertices_out_[1]]
            )
    # 4. 3 vertices in:
    if vertices_in == 3:
        v_out_ind = vertices_out_[0]
        v_out = vertices[v_out_ind]
        return 1 - corner_area(r, x_, y_, *get_corner_points(v_out_ind, points_on_sides), v_out)


def lr(i1: int, i2: int):
    return (i1, i2) if i2 - i1 in [1, -3] else (i2, i1)


def get_corner_points(vertex_ind: int, points_segments_on_sides: dict) -> tuple[
    tuple[float, float], tuple[float, float]]:
    points_on_side = points_segments_on_sides[(vertex_ind + 3) % 4]
    return points_segments_on_sides[vertex_ind][0], points_on_side[1] if len(points_on_side) > 1 else points_on_side[0]


def trapeze_area(a: float, b: float, h: float):
    return (a + b) * h / 2


def corner_area(r: float, cx: float, cy: float, p1: tuple[float, float], p2: tuple[float, float],
                v: tuple[float, float]):
    area = area_heron(v, p1, p2) - segment_area(r, cx, cy, p1, p2)
    return area


def get_angle_radians(v1: tuple[float, float], v2: tuple[float, float]):
    return abs(math.acos((v1[0] * v2[0] + v1[1] * v2[1]) / (math.hypot(*v1) * math.hypot(*v2))))


def circle_area(r: float):
    return sector_area(r, 2 * math.pi)


def area_heron(p1: tuple[float, float], p2: tuple[float, float], p3: tuple[float, float]):
    """computes the triangle's area, using the formula of Heron"""
    a, b, c = math.hypot(p1[0] - p2[0], p1[1] - p2[1]), math.hypot(p2[0] - p3[0], p2[1] - p3[1]), math.hypot(
        p3[0] - p1[0], p3[1] - p1[1])
    p = (a + b + c) / 2
    return (p * (p - a) * (p - b) * (p - c)) ** .5

    # 36.6 98


def sector_area(r: float, angle: float):
    return angle * r ** 2 / 2


def segment_area(r: float, cx: float, cy: float, p1: tuple[float, float], p2: tuple[float, float]):
    area = (s := sector_area(r, a := get_angle_radians((p1[0] - cx, p1[1] - cy), (p2[0] - cx, p2[1] - cy)))) - (
        t := area_heron((cx, cy), p1, p2))
    return area


def get_points_of_intersection(r: float, cx: float, cy: float):
    points_on_sides = {0: [], 1: [], 2: [], 3: []}
    # x = 0:
    if cx <= r:
        d_ = (r ** 2 - cx ** 2) ** .5
        if cy - d_ >= 0:
            points_on_sides[0].append((0, cy - d_))
        if cy + d_ <= 1:
            points_on_sides[0].append((0, cy + d_))
    # y = 1:
    if (1 - cy) <= r:
        d_ = (r ** 2 - (1 - cy) ** 2) ** .5
        if cx - d_ >= 0:
            points_on_sides[1].append((cx - d_, 1))
        if cx + d_ <= 1:
            points_on_sides[1].append((cx + d_, 1))
    # x = 1:
    if (1 - cx) <= r:
        d_ = (r ** 2 - (1 - cx) ** 2) ** .5
        if cy + d_ <= 1:
            points_on_sides[2].append((1, cy + d_))
        if cy - d_ >= 0:
            points_on_sides[2].append((1, cy - d_))
    # y = 0:
    if cy <= r:
        d_ = (r ** 2 - cy ** 2) ** .5
        if cx + d_ <= 1:
            points_on_sides[3].append((cx + d_, 0))
        if cx - d_ >= 0:
            points_on_sides[3].append((cx - d_, 0))
    # returns all the correct points on sides:
    return points_on_sides


def get_pars():
    n, r = input().split()
    n = int(n)
    r = float(r)
    points = []
    for _ in range(n):
        x, y = map(float, input().split())
        points.append((x, y))
    return n, r, points


def main():
    get_math_exp()


if __name__ == '__main__':
    main()


# num_ = 1_000
# points_ = [(random.randint(0, num_) / num_, random.randint(0, num_) / num_) for _ in range(100_000)]  # 36.6 98
# print(points_)
# get_math_exp(0.7, points_)

# print(f'res: {get_math_exp_1_point(0, 0.5, 0.75)}')


