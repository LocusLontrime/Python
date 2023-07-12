# accepted on coderun
import math


def calc_area():
    n, m, ls, f_coeffs, rs, g_coeffs = get_pars()
    f_counter, g_counter = 1, 1
    area = 0.0
    lb = ls[0]
    while lb < ls[n]:
        if ls[f_counter] == rs[g_counter]:
            rb = ls[f_counter]
            area += step_area(lb, rb, f_coeffs[f_counter - 1], g_coeffs[g_counter - 1])
            f_counter += 1
            g_counter += 1
        elif ls[f_counter] < rs[g_counter]:
            rb = ls[f_counter]
            area += step_area(lb, rb, f_coeffs[f_counter - 1], g_coeffs[g_counter - 1])
            f_counter += 1
        else:
            rb = rs[g_counter]
            area += step_area(lb, rb, f_coeffs[f_counter - 1], g_coeffs[g_counter - 1])
            g_counter += 1
        lb = rb
    print(f'{area}')


def step_area(lb: int, rb: int, f_abc: tuple[int, int, int], g_abc: tuple[int, int, int]) -> float:
    # coeffs of (f-g)(x) func:
    fga, fgb, fgc = map(sub, f_abc, g_abc)
    # roots array:
    roots = []
    # roots computing:
    if fga != 0:
        d = fgb ** 2 - 4 * fga * fgc
        # quadratic polynom:
        if d == 0:
            roots.append(- fgb / (2 * fga))
        elif d > 0:
            roots.append((- fgb + math.sqrt(d)) / (2 * fga))
            roots.append((- fgb - math.sqrt(d)) / (2 * fga))
    elif fgb != 0:
        # linear polynom:
        roots.append(- fgc / fgb)
    # let us validate the roots at interval [lb, rb]:
    roots = [root for root in roots if lb < root < rb]
    # integral computing:
    roots = sorted(roots + [lb, rb])
    area = sum(integrate(roots[_], roots[_ + 1], fga, fgb, fgc) for _ in range(len(roots) - 1))
    # returns res:
    return area


def integrate(lb: float, rb: float, fga: int, fgb: int, fgc: int) -> float:
    return abs(fga * (rb ** 3 - lb ** 3) / 3 + fgb * (rb ** 2 - lb ** 2) / 2 + fgc * (rb - lb))


def sub(a, b):
    return a - b


def get_pars():
    n, m = map(int, input().split())
    ls = [int(_) for _ in input().split()]
    f_coeffs = [tuple(int(_) for _ in input().split()) for _ in range(n)]
    rs = [int(_) for _ in input().split()]
    g_coeffs = [tuple(int(_) for _ in input().split()) for _ in range(m)]
    return n, m, ls, f_coeffs, rs, g_coeffs


calc_area()


















                                                                                      # 36.6 98









