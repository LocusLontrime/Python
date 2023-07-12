# accepted on coderun
import fractions
import functools
import sys
# OPTIMIZED VERSION ------->>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
sys.setrecursionlimit(100_000)


memo_table = {}


def min_m_exp(n, ints):
    n, ints = get_pars(n, ints)
    ints = sorted(ints)
    m_exp_t = integrate(1, n - 1, ints) / fractions.Fraction(functools.reduce(lambda x, y: y * x, ints, 1))
    # print(f'{m_exp_t}') if m_exp_t.denominator > 1 else print(f'{m_exp_t}/{1}')
    print(f'num: {m_exp_t.numerator}')
    print(f'den: {m_exp_t.denominator}')


def integrate(pow_: int, ind_: int, ints: list[int]) -> fractions.Fraction:
    """recursive math exp computer, requires ints array to be sorted in ascending order"""
    global memo_table
    # print(f'pow_: {pow_}, ind_: {ind_}, interval_: {ints[ind_]}')
    # base case:
    if ind_ == 0:
        return ints[0] ** (pow_ + 1) / fractions.Fraction(pow_ + 1)
    if (pow_, ind_) not in memo_table.keys():
        # recurrent relation:
        cl = fractions.Fraction(ints[ind_])
        left = cl * integrate(pow_, ind_ - 1, ints)
        cr = fractions.Fraction(pow_, pow_ + 1)
        right = cr * integrate(pow_ + 1, ind_ - 1, ints)
        # print(f'cl: {cl}, cr: {cr}')
        # print(f'left: {left}, right: {right}')
        memo_table[(pow_, ind_)] = left - right
    return memo_table[(pow_, ind_)]


def get_pars(n, ints):
    # n = int(input())
    # ints = [int(_) for _ in input().split()]
    return n, ints


n_ = 964
ints_ = [_ for _ in range(1, n_ + 1)]

min_m_exp(n_, ints_)
