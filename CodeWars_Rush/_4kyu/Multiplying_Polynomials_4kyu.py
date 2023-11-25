# accepted on codewars.com
import re
from collections import defaultdict as d


def polynomial_product(polynomial_1: str, polynomial_2: str) -> str:
    polynomial_1 = polynomial_1.replace(' ', '')
    polynomial_2 = polynomial_2.replace(' ', '')
    poly1, poly2 = map(pars_poly, [polynomial_1, polynomial_2])
    product = d(int)
    for pow1 in poly1.keys():
        for pow2 in poly2.keys():
            product[pow1 + pow2] += poly1[pow1] * poly2[pow2]
    product = {k: v for k, v in product.items() if v != 0}
    s1, s2 = re.findall(r'[a-zA-Z]+', polynomial_1), re.findall(r'[a-zA-Z]+', polynomial_2)
    res = to_string(product, set(s1) | set(s2))
    print(res)
    return res


def pars_poly(polynomial: str) -> dict[int, int]:
    pattern_mono, pattern_digs, pattern_letters = r'[+-]?[^-+]+', r'\d+', r'[a-zA-Z]+'
    monomials: list[str] = re.findall(pattern_mono, polynomial)
    poly = d(int)
    for monomial in monomials:
        if monomial:
            multiplier = -1 if monomial[0] == '-' else 1
            monomial = monomial.split('^') if (flag := '^' in monomial) else [monomial]
            coeff = int(coeff[0]) if (coeff := re.findall(pattern_digs, monomial[0])) else 1
            power = int(re.findall(pattern_digs, monomial[1])[0]) if flag else 1 if re.findall(pattern_letters, monomial[0]) else 0
            poly[power] = coeff * multiplier
    return poly


def to_string(poly: dict[int, int], var: set[str]) -> str:
    pol_str, variable = '', f'{var.pop() if var else f"x"}'
    if len(poly) == 0:
        return '0'
    for i, (power_key, coeff) in enumerate(sorted(poly.items(), key=lambda x: -x[0])):
        if i != 0:  # not for leading power
            pol_str += '+' if coeff > 0 else '-'
        else:
            pol_str += '-' if coeff < 0 else ''
        pol_str += str(abs(coeff)) if abs(coeff) != 1 else '' if power_key != 0 else '1'
        pol_str += variable if power_key != 0 else ''
        pol_str += '^' + str(power_key) if power_key > 1 else ''


# pars_poly(f'3v^5+v^4+3v^3-x-1')
print(f'product: {polynomial_product("F + 1", "F - 1")}')  # f"3v^5+v^4+3v^3-x-1", f"7v^2+1" | "x^2", "3x - 1" | "0", "2-x"
