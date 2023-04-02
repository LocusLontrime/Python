def calculate(rectangles_: list[tuple[int, int, int, int]]):
    print(f'rectangles: ')
    for rectangle in rectangles_:
        print(f'{rectangle}')


def area(a, b, c, d):
    return (c - a) * (d - b)


def covering_rect(rects):
    return (min(r[0] for r in rects),
            min(r[1] for r in rects),
            max(r[2] for r in rects),
            max(r[3] for r in rects))


def clip(bb, rects):
    if not rects:
        return []
    (x1, y1, x2, y2) = rects[0]
    rs = rects[1:]
    (a1, b1, a2, b2) = bb
    if a1 == a2 or b1 == b2:
        return []
    if a1 >= x2 or a2 <= x1 or y1 >= b2 or y2 <= b1:
        return clip(bb, rs)
    return [(max(a1, x1), max(b1, y1), min(a2, x2), min(b2, y2))] + clip(bb, rs)


def calc(cr, rects):
    if not rects:
        return 0

    rc = rects[0]
    rs = rects[1:]
    x1, y1, x2, y2 = cr
    l1, m1, l2, m2 = rc
    t = (x1, m2, x2, y2)
    b = (x1, y1, x2, m1)
    l = (x1, m1, l1, m2)
    r = (l2, m1, x2, m2)
    return area(*rc) + sum(calc(x, clip(x, rs)) for x in [t, b, l, r])


rectangles = [
    (1, 2, 6, 6),
    (1, 3, 5, 5),
    (1, 1, 7, 7)
]

r_x = []


print(f'res: {calc(covering_rect(rectangles), rectangles)}')
