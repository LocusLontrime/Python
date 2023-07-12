# accepted on coderun
import math
import sys
from collections import defaultdict as d
import time


symbols = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ'
symbols_ = {symbols[_]: _ for _ in range(len(symbols))}
modulo = 100000007


def min_base(s: str):
    m, coefficients = get_pars(s)
    print(f'm: {m}')
    start_ = time.time_ns()
    max_length = max(coefficients.keys()) + 1
    print(f'coefficients: {coefficients}')
    # adding the keys skipped:
    for key in range(max_length):
        if key not in coefficients.keys():
            coefficients[key] = 0
    # removing 'leading' zero coeffs:
    ind_ = 0
    while ind_ < max_length and coefficients[ind_] == 0:
        ind_ += 1
    # changing the coefficients' dict:
    coefficients = {_ - ind_: coefficients[_] for _ in range(ind_, max_length)}
    print(f'fixed coefficients: {coefficients}')
    if len(coefficients) == 0:
        finish_ = time.time_ns()
        print(f'math time elapsed: {(finish_ - start_) // 10 ** 6} milliseconds')
        return m
    # factorization of a free term:
    factors = factorize(c := abs(coefficients[0]))
    print(f'c: {c}')
    print(f'factors: {factors}')
    for factor_ in factors:
        if factor_ >= m:
            if is_root(coefficients, factor_):
                finish_ = time.time_ns()
                print(f'math time elapsed: {(finish_ - start_) // 10 ** 6} milliseconds')
                return factor_
    finish_ = time.time_ns()
    print(f'math time elapsed: {(finish_ - start_) // 10 ** 6} milliseconds')
    return -1


def factorize(num: int) -> list[int]:
    factors = set()
    f_ = 2
    while f_ ** 2 <= num:
        if num % f_ == 0:
            factors.add(f_)
            factors.add(num // f_)
        f_ += 1
    factors.add(num)
    return sorted(factors)


def is_root(coefficients: dict[int, int], root: int) -> bool:
    temporal = 0
    for i in range(len(coefficients) - 1, -1, -1):
        cell = temporal * root + coefficients[i]
        temporal = cell
    return not temporal


def get_pars(s: str) -> tuple[int, dict[int, int]]:
    # a string equation given:
    min_base_possible = 2
    k = 1  # aux multiplier for the rights
    ind_ = len(s) - 1  # common sequence index for the string s
    # max_length = 0
    coefficients = d(int)
    while ind_ >= 0:
        # print(f'i: {ind_}')
        # whitespaces removing:
        while ind_ >= 0 and s[ind_] == ' ':
            ind_ -= 1
        # parsing current num:
        _ind = ind_
        while ind_ >= 0 and s[ind_].isalnum():
            # print(f'a_: {a}')
            ind_ -= 1
        # max_length = max(max_length, _ind - ind_)  # ???
        ind_saved = ind_
        # print(f'ind_: {ind_}, num_: {s[ind_ + 1: _ind + 1]}')
        # whitespaces removing:
        while ind_ >= 0 and s[ind_] == ' ':
            ind_ -= 1
        # leftmost symbol past:
        signum = s[ind_]
        if signum == '-':
            multiplier = -1
        else:
            multiplier = 1
        ind_ -= 1
        # print(f'multiplier: {multiplier}, k: {k}')
        m_ = multiplier * k
        for i_ in range(_ind, ind_saved, -1):
            coefficients[_ind - i_] += symbols_[a := s[i_]] * m_
            min_base_possible = max(min_base_possible, symbols_[a] + 1)
        # k changing:
        if signum == '=':
            k = -1
    return min_base_possible, coefficients


def translate_to_decimal(num: str, _base: int) -> int:
    return sum(symbols_[symbol] * _base ** (len(num) - 1 - ind) for ind, symbol in enumerate(num))


def get_val_mod(coeffs: dict[int, int], n: int) -> int:
    return sum((coeffs[_] * pow(n, _, modulo)) for _ in range(len(coeffs))) % modulo


def main():
    print(f'{min_base(...)}')


s_ = '+'.join(['Z' for _ in range(25 * 10 ** 4)]) + '=' + 'Z' + '-'.join(['Z' for _ in range(25 * 10 ** 4)])
s__ = '+'.join(['Z' * 10 ** 5 for _ in range(5)]) + '=' + 'Z' + '-'.join(['Z' * 10 ** 5 for _ in range(5)])  # ???
s___ = 'Z' * 5 * 10 ** 5 + '=' + 'Z' * 5 * 10 ** 5
s_x = '1 = 1'
s_neo = f"P3VWB2L+18YIH6+2ST6TDRI9=2X+BRH+GXAU-D20S8R+2TIOZS45J"

start = time.time_ns()
print(f'{min_base(s_)}')  # f"F4240 + 7A120 = 16E360"
finish = time.time_ns()
print(f'time elapsed: {(finish - start) // 10 ** 6} milliseconds')


def key_(y: int, x: int):
    return math.pi - math.atan2(x, -y)


