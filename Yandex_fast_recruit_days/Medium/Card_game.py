# accepted on coderun
import sys
import fractions
import time

modulo = 10 ** 9 + 7
combs_restr_memo = {}
combs_precalced = {}
max_a = 10
start: int


def drawn_probability():
    global start
    n, quantities = get_pars()
    start = time.time_ns()
    pre_calc()
    sum_ = sum(quantities)
    pos_outcomes = combinations_with_restrictions(sum_ // 2, 0, 0, 0, quantities)
    all_outcomes = combinations(sum_ // 2, sum_)
    f = fractions.Fraction(pos_outcomes, all_outcomes)
    print(f'f: {f}')
    p, q_inv = f.numerator, mod_inverse(f.denominator, modulo)
    print(f'{(p * q_inv) % modulo}')


def pre_calc():
    global combs_precalced
    for n_ in range(0, max_a + 1):
        for k_ in range(0, n_ + 1):
            combs_precalced[(k_, n_)] = combinations(k_, n_)


def combinations(k: int, n: int):
    k = max(k, n - k)
    combs = 1
    for i in range(k + 1, n + 1):
        combs = combs * i // (i - k)
    return combs


def combinations_with_restrictions(k_: int, index_: int, zeroed: int, non_touched: int, quantities_: list[int]) -> int:
    global combs_restr_memo
    key_ = (k_, index_, zeroed - non_touched)
    # border case:
    if k_ < 0:
        return 0
    if index_ == len(quantities_):
        if zeroed == non_touched:
            if k_ == 0:
                return 1
        return 0
    # body of recursion:
    if key_ not in combs_restr_memo:
        res = 0
        for i_ in range(0, (q := quantities_[index_]) + 1):
            # recurrent relation:
            res += combs_precalced[(i_, q)] * combinations_with_restrictions(
                k_ - i_,
                index_ + 1,
                zeroed + (1 if i_ == q else 0),
                non_touched + (1 if i_ == 0 else 0),
                quantities_
            )
        combs_restr_memo[key_] = res
    # returning result:
    return combs_restr_memo[key_]


def mod_inverse(a: int, mod: int) -> int:
    g, x, y = gcd_extended(a, mod)
    if g != 1:
        raise ValueError(f'no modular inverse element exists!!!')
    else:
        return (x % mod + mod) % mod


def gcd_extended(a: int, b: int):
    if a == 0:
        return b, 0, 1
    d, x, y = gcd_extended(b % a, a)
    return d, y - (b // a) * x, x


def get_pars():
    n = int(input())
    quantities = [int(_) for _ in input().split()]
    return n, quantities


def main():
    drawn_probability()


if __name__ == '__main__':
    main()
    finish = time.time_ns()
    print(f'time elapsed: {(finish - start) // 10 ** 6} milliseconds')


# combs_ = sum(combinations(_, 20) for _ in range(1, 6 + 1))
# print(f'combs: {combs_}')





                                                                                      # 36.6 98









