# accepted on codewars.com
import time
# 10 -> base of numeral system, 9 -> max integer in decimal system
memo_table: dict[tuple[int, int, int], tuple[int, int]] = {}


def jump_to_zero(arr: list[int]):
    return [rec_seeker(length := len(str(n_)), 0, 0, True, get_digs_str(n_), n_, length)[0] for n_ in arr]


def rec_seeker(i: int, sum_: int, shift_: int, restr: bool, digits: list[int], num: int, length: int) -> tuple[int, int]:
    if (i, sum_, shift_) not in memo_table.keys():
        # border case:
        if i <= len(str(9 * length)):  # digits remained to the right
            r = i_am_brut(sum_, num % (10 ** i) if restr else 10 ** i + shift_)
            if not restr:
                memo_table[(i, sum_, shift_)] = r
            return r
        # body of rec:
        res, interim_res = 0, 0
        next_shift = shift_
        max_dig = digits[length - i] if restr else 9
        for d_ in range(max_dig, -1, -1):  # from 9 to zero
            # recurrent relation
            interim_res, next_shift = rec_seeker(i - 1, sum_ + d_, next_shift, restr and d_ == max_dig, digits, num, length)
            res += interim_res
        r = res, next_shift
        if not restr:
            memo_table[(i, sum_, shift_)] = r
        return r
    # returning value:
    return memo_table[(i, sum_, shift_)]


def i_am_brut(sum_: int, num: int) -> tuple[int, int]:
    steps = 0
    while num >= 0 and (num != 0 or sum_ != 0):
        num, steps = num - sum_ - sum_digs(num), steps + 1
    return steps, num


def sum_digs(n: int) -> int:
    return sum(map(int, str(n)))


def get_digs_str(n: int):
    return [int(d) for d in str(n)]


arrays = [[k * 10 ** 18 for k in range(1_000)]]  # i * 10 ** 18 for i in range(98)
start = time.time_ns()
for arr_ in arrays:
    res_ = jump_to_zero(arr_)
    # print(f'STEPS: {res_}')  # 10 ** x for x in range(18 + 1)
finish = time.time_ns()
print(f'time elapsed str: {(finish - start) // 10 ** 6} milliseconds')
print(f'MEMO TABLE: ')
for key in sorted(memo_table.keys(), key=lambda k: (k[0], -k[1], -k[2])):
    print(f'{key}: {memo_table[key]}')
print(f'SIZE: {len(memo_table)}')


# RES: [1, 2, 11, 81, 611, 4798, 39320, 333583, 2897573, 25632474]

# steps per 100k -->> [4798, 9350, 13681, 17811, 21760, 25544, 29179, 32680, 36057, 39320]
























