# accepted on coderun
import fractions
import math
import sys
import threading


def prob():
    n, k = get_pars()
    digits = [int(_) for _ in n]
    length = len(digits)
    print(f'n: {n}')
    print(f'k: {k}')
    print(f'digits: {digits}')
    # divisibility by 3 is an invariant among the set of all the possible digits' permutations:
    div_by_3 = sum(digits) % 3 == 0
    print(f'div_by_3: {div_by_3}')
    # as the number given contains no zeroes -> it won't be divisible by 10 after any possible number of permutations
    # it means that we should pay attention to the last right digit after the every probable permutation and check if it equals 2 or 5...
    # the exit condition:
    if 5 not in digits and (all(_ % 2 != 0 for _ in digits) or not div_by_3):
        print(f'ZERO PROB FOR ANY K!!!')
        return 0.0
    # let us count all the good digits, it means the digits that makes the number given divisible by one of the two favourite Sasha's numbers (5 or 6)
    # if any of them (digits) stays at the rightmost place -> .......d, when d symbolizes a good digit
    good_digs_q = digits.count(5) + (sum(1 for _ in digits if _ % 2 == 0) if div_by_3 else 0)
    print(f'good_digs_q: {good_digs_q}')
    # we need to define the start position: whether it good (permuted number_ is divisible by 5 or 6) or not:
    last_dig = digits[-1]
    print(f'last_dig: {last_dig}')
    start_pos = (last_dig % 2 == 0 and div_by_3) or last_dig == 5  # True or False
    print(f'start_pos: {start_pos}')
    perms = permuts(length - 1)
    print(f'perms: {perms}')
    ll, ml, mr, rr = perms - good_digs_q, good_digs_q, length - good_digs_q, perms - (length - good_digs_q)
    print(f'll, ml, mr, rr: {ll, ml, mr, rr}')
    # the main logic:
    probability = tree_prob(k, ll, ml, mr, rr, perms, not start_pos)
    print(f'probability: {probability}')
    return float(probability)


def permuts(elems_q: int) -> int:
    return elems_q * (elems_q + 1) // 2


def get_pars() -> tuple[str, int]:
    n = input()
    k = int(input())
    return n, k


def tree_prob(level: int, ll: int, ml: int, mr: int, rr: int, perms: int, start: bool) -> fractions.Fraction:
    memo = dict()

    def rec_tree_calc(neg: bool, depth_: int) -> int:
        print(f'neg: {neg}, depth_: {depth_}')
        if (neg, depth_) not in memo.keys():
            # border case:
            if depth_ == level:
                # ???
                return 0 if neg else 1
            # body of rec:
            (left, right) = ((ll, ml) if neg else (mr, rr))
            # recurrent relation:
            print(f'left: {left}, right: {right}')
            memo[(neg, depth_)] = left * rec_tree_calc(True, depth_ + 1) + right * rec_tree_calc(False, depth_ + 1)
        return memo[(neg, depth_)]

    numerator = rec_tree_calc(start, 0)
    denominator = perms ** level
    print(f'numerator: {numerator}')
    print(f'denominator: {denominator}')

    return fractions.Fraction(numerator, denominator)


print(f'probability: {prob()}')
