import sys
import threading
import time


# bitmasks:
whites: int
blacks: int


def solve_line(line: str, groups: list[int]) -> str:
    global whites, blacks
    ll, gl = len(line), len(groups)
    whites = 0  # [0 for _ in range(ll + 1)]
    blacks = 0  # [0 for _ in range(ll + 1)]
    # buiding prefix arrays:
    prefix_whites = [0 for _ in range(ll + 1)]
    # prefix_blacks = [0 for _ in range(ll + 1)]
    for i in range(ll):
        prefix_whites[i + 1] = prefix_whites[i] + (1 if line[i] == '.' else 0)
        # prefix_blacks[i + 1] = prefix_blacks[i] + (1 if line[i] == 'X' else 0)
    # print(f'prefix_whites: {prefix_whites}')
    # print(f'prefix_blacks: {prefix_blacks}')
    memo_table = {}
    print(f'll, gl: {ll, gl}')
    dp(0, 0, False, 1, ll, gl, line, groups, prefix_whites, memo_table)
    print(f'whites: {whites}')
    print(f'blacks: {blacks}')
    # line recovering:
    print(f'memo size: {len(memo_table)}')
    res = f''
    pow2 = 1
    for i in range(ll):
        if whites & pow2 and blacks & pow2:
            res += f'?'
        elif whites & pow2:
            res += f'.'
        elif blacks & pow2:
            res += f'X'
        else:
            return '-1'
        pow2 <<= 1
    return res


def dp(n: int, k: int, black: bool, num: int, ll: int, gl: int, line: str, groups: list[int], prefix_whites: list[int], memo_table: dict[tuple[int, int, int], bool]) -> bool:
    global whites, blacks
    # print(f'n, k, black: {n, k, black}')
    # border cases:
    if n > ll:
        return False
    if n == ll:
        if k == gl:
            return True
        else:
            return False
    res = False
    if (n, k, black) not in memo_table.keys():
        # main part:
        # 1. whites check:
        if line[n] != 'X':
            # print(f'...white placing: ')
            if dp(n + 1, k, False, num << 1, ll, gl, line, groups, prefix_whites, memo_table):
                whites |= num
                res = 1
        # 2. blacks check:
        if k < gl:
            if not black:
                if n + groups[k] <= ll:
                    # print(f'...black placing:')
                    # print(f'......prefix_whites[{n}]: {prefix_whites[n]}')
                    # print(f'......prefix_whites[{n - groups[k - 1]}]: {prefix_whites[n - groups[k - 1]]}')
                    if prefix_whites[n + (grk := groups[k])] - prefix_whites[n] == 0:
                        if dp(n + grk, k + 1, True, num_ := num << grk, ll, gl, line, groups, prefix_whites, memo_table):
                            # print(f'.........n: {n}')
                            blacks |= num_ - num
                            res = 1
        memo_table[(n, k, black)] = res
    # returns res:
    return memo_table[(n, k, black)]


def main():
    m = 100
    groups_ = [_ for _ in range(1, m + 1)]  # 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13
    line_ = f'?' * (s := sum(groups_) + m - 1)
    start = time.time_ns()
    print(f'res: {solve_line(line_, groups_)}')
    finish = time.time_ns()
    print(f's: {s}')
    print(f'time elapsed: {(finish - start) // 10 ** 6} milliseconds')


thread = threading.Thread(target=main)
sys.setrecursionlimit(1_000_000)
threading.stack_size(0x8000000)
thread.start()                                                                        # 36 366 98 989 LL


# bit = 4  # 16 + 8
# mask = 0b11000  # 16
# print(f'result: {mask & bit}')
# mask = mask | bit
# print(f'new mask: {mask}')
# print(f'result: {mask & bit}')

mask_ = 0
mask_ |= 7
print(f'mask_: {mask_}')
print(f'{0 | 7}')
k_ = 2
k_ = (k_ << 3)
print(f'res_: {k_}')



