# accepted on codewars.com
import math
from fractions import Fraction


def decompose(n):
    fraction = Fraction(n)
    print(f'fraction: {fraction}')
    p, q = fraction.numerator, fraction.denominator
    print(f'p, q: {p, q}')
    # base cases:
    if p == 0:
        return []
    if p % q == 0:
        return [f'{p // q}']
    result = []
    # simplification of the fraction given:
    gcd = math.gcd(p, q)
    p //= gcd
    q //= gcd
    # an integer part:
    if p > q:
        int_part = get_int_part(p, q)
        result.append(f'{int_part}')
        p -= int_part * q
    egyptians = []
    rec_seeker(p, q, egyptians)
    for egyptian in egyptians:
        result.append(f'1/{egyptian}')
    return result


def rec_seeker(p, q, egyptians):
    # border case:
    if p == 1:
        egyptians.append(q)
        return
    # body of rec:
    int_part_min = q // p + 1
    egyptians.append(int_part_min)
    p_new = p * int_part_min - q
    q_new = q * int_part_min
    # simplification:
    gcd = math.gcd(p_new, q_new)
    # new numerator and denominator of rest fraction:
    p_new //= gcd
    q_new //= gcd
    #reccurent relation:
    rec_seeker(p_new, q_new, egyptians)


def get_int_part(p, q):
    return p // q


print(f'{decompose("11769791/1178892117111117")}')

