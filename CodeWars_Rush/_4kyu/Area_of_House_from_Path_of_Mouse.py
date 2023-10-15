# accepted on codewars.com
import time
from collections import namedtuple as nt
dydx = ((0, 1), (-1, 0), (0, -1), (1, 0))


def mouse_path(s: str):
    vertices, f1, f2 = parse_coords(s)
    length = len(vertices)
    print(f'vertices: {vertices}')
    print(f'v_len: {length}')
    # Intersections check:
    for j in range(len(vertices)):
        for i in range(j - 1):
            if (j != length - 1 or i != 0) and is_intersect(vertices[j], vertices[(j + 1) % length], vertices[i], vertices[(i + 1) % length]):
                print(f'ERROR at j, i: {j, i}')
                return None
    # Gauss formula:
    area = sum(v.x * vertices[(i + 1) % length].y - v.y * vertices[(i + 1) % length].x for i, v in enumerate(vertices)) // 2
    print(f'area, f1, f2: {area, f1, f2}')
    return (abs(area) if area != 0 else None) if f1 and f2 else None


def is_intersect(p1s: nt, p1e: nt, p2s: nt, p2e: nt):
    x_collinear = p1s.x == p1e.x == p2s.x == p2e.x
    y_collinear = p1s.y == p1e.y == p2s.y == p2e.y
    if x_collinear:
        # 'collinear' case:
        intersection = min(p1s.y, p2s.y) <= max(p1s.y, p2s.y) <= min(p1e.y, p2e.y)
    elif y_collinear:
        intersection = min(p1s.x, p2s.x) <= max(p1s.x, p2s.x) <= min(p1e.x, p2e.x)
    else:
        # orthogonal case:
        if p2s.y == p2e.y:
            intersection = min(p2s.x, p2e.x) <= p1s.x <= max(p2s.x, p2e.x) and min(p1s.y, p1e.y) <= p2s.y <= max(p1s.y, p1e.y)
        else:
            intersection = min(p1s.x, p1e.x) <= p2s.x <= max(p1s.x, p1e.x) and min(p2s.y, p2e.y) <= p1s.y <= max(p2s.y, p2e.y)
    return intersection


def parse_coords(s) -> tuple[list[nt], bool, bool]:                                                      # 36.6 98
    length = len(s)
    print(f's_length: {length}')
    ind_ = 0
    y_, x_ = 0, 0
    d_ = 0
    vertices = []
    while ind_ < length:
        if ind_ != 0:
            dir_ = -1 if s[ind_] == 'L' else 1
            d_ = (d_ + dir_) % len(dydx)
            ind_ += 1
        temp = ind_
        while ind_ < length and s[ind_].isdigit():
            ind_ += 1
        num_ = int(s[temp: ind_])
        y_ += num_ * dydx[d_][0]
        x_ += num_ * dydx[d_][1]
        t_ = nt('Point', ['y', 'x'])
        vertices.append(t_(y_, x_))
    return vertices, (y_, x_) == (0, 0), d_ != 0


s_ = '4L10L20L30L30L50L40L60L60L85L77L10L67R72R45R47R33R30R17R15R5R5'  # 2950
s__ = '10R5R5R10L5L5'  # None
s___ = '12R6R2R2R1L1L1R2L1L1R4R2L1L5R1L3R6R2R1L2R2L4'  # None
s_x = '2L15L1R12R1L20L3R1L5R1R3L2L1R2R2L1L2R1R2L3L2R1L2R2R4L3L3R1L1R3L5L10R15R20L20R20R15L1R1L3R3L1L3R1R2L1L1R2L2R1L25R10R10L10L10R10R10L10L10R10R10L10R5L30R10L10R5L50R10R10L15L10R15R10L10L40R15R60L5R20L30R20R5L30R5L30R10L30L20R20R30L10R5L60R10R60L10L10R10L60R1R6L3L6R1R2L4'  # None
s_z = '158R10R241L2R29L10L253R19R287L27L7R2L48R19L169R10R273L14L279R3R2L14R145L22R102L22L272R25R102L3R79L7R11L27R115L7L119R8L29R16L33R2R182L4L224R10L18R27R209L6L157R10R9L1R97L6R7L16L195R4R261L12L186R7L145R20R244L27L7R7L34R13L68R1R86L8R145L37R14L325R14R161L10R77L17L148R23L6R23R205L2L30R18L140R28R7L12R225L23L333R2L43R2R232L2L199R14R318L21L218R3R78L14L164R21R219L20R99L3L85R22L145R18R100L17L61R1R158L7R3L8L226R6R86L11R113L9L199R15R37L24R202L13L18R15L152R11L91R25R4L2R68L4L69R8R68L13R142L6L199R8R40L26L119R17R245L1L218R1R233L20R18L18L197R17R273L26L3R19L169R25L115R10R112L11R45L18L12R9L215R18R128L5R140L19R100L27R24L71R8R42L12L323R1R86L18R254L3L143R14R33L3R128L10R18L21L316R7R313L10L122R7R123L25L19R7L210R10R22L18L30R6L133R10R325L9L74R11R30L12L47R20L128R11R117L20L98R24R101L3L112R16R242L19L337R9R27L9R72L9R90L12L159R23R284L8L242R20L22R11R175L7L18R26L89R1L82R14R310L12L109R9R21L3L120R21L79R9R75L20R210L6L339R17L23R19R48L20R164L14L26R18R38L27R79L2L74R12R33L24R105L23L167R3R174L113R1L108R12L47R18L40R4R104L19L53R26R189L25L294R26R328L27L328R4L17R16R32L22R52L7R73L4R217L6L81R10R22L4L196R24R11L18R57L11R4L16R18L3R31L22R65L5R6L23L119R17L37R4R169L10L296R7R309L17L110R6R78L8L220R15L48R25R147L25R74L4L240R11R322L18L224R17L57R1L46R6R197L6R2L26L17R14L127R14R33L11R137L12L55R1R189L15L257R5L95R24R187L3L177R2L29R27R308L8L68R28L88R18L135R8R195L23R166L90R23L221R8R118L21R123L2L220R5R276L13L333R11R244L22R29L18R65L5L223R6R80L23L139R11R151L16L48R15L193R26R297L9L151R11L62R3L34R4R12L12R49L3R214L7L324R10R281L17L42R14L84R4'  # 1191080
start = time.time_ns()
print(f'area: {mouse_path(s_z)}')
finish = time.time_ns()
print(f'time elapsed: {(finish - start) // 10 ** 6} milliseconds')
