# accepted on coderun
import sys


def length():
    s, q, requests = get_pars()
    ind_ = 0
    suffix_arr = []
    aggregated_length, aggregated_delta = 0, 0
    res = []
    while ind_ < (w := len(s)):
        # parsing a number:
        _ind = ind_
        while ind_ < w and s[ind_].isdigit():
            ind_ += 1
        num_ = s[_ind: ind_]
        # parsing a symbol:
        ind_ += 1
        # appending results to the suffixes array:
        num = int(num_) if num_ else 1
        suffix_arr.append((aggregated_length, aggregated_delta))
        aggregated_length += num
        aggregated_delta += ind_ - _ind
    for l_, r_ in requests:
        lb = bin_search(suffix_arr, l_ - 1)
        rb = bin_search(suffix_arr, r_ - 1)
        if rb > lb:
            lb_suff = suffix_arr[lb + 1]
            rb_suff = suffix_arr[rb]
            r = (-lb_suff[1] + rb_suff[1]) + get_len(lb_suff[0] - (l_ - 1)) + get_len(r_ - rb_suff[0])
        else:
            r = get_len(r_ - l_ + 1)
        res.append(str(r))
    return '\n'.join(res)


def get_len(a: int):
    return 0 if a == 0 else (0 if a == 1 else len(str(a))) + 1


def get_pars() -> tuple[str, int, list[list[int]]]:
    s = input()
    q = int(input())
    requests = [[int(_) for _ in input().split(' ')] for _ in range(q)]
    return s, q, requests


def bin_search(array: list[tuple[int, int]], el: int) -> int:
    lb, rb = 0, len(array) - 1
    while lb <= rb:
        mb = (lb + rb) // 2
        m, _ = array[mb]
        if el < m:
            rb = mb - 1
        else:
            lb = mb + 1
    return lb - 1


def main():
    print(length())


if __name__ == '__main__':
    main()
