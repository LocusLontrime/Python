import math


def get_winner():
    n, m, numbers = get_pars()
    # main cycle:
    sums: list[int, int] = [0, 0]  # bokas_sum, zhokas_sum = 0, 0
    i_ = 0
    turn = 0
    while i_ < n:
        # defining best strategy:
        indices_ = []
        is_max_ = True
        pairs_ = []
        best_max_sum_ = ...
        for index_ in indices_:
            max_sum_, max_indices_ = get_max_data(index_, min(index_ + m, n), numbers, is_max_)
            pairs_.append((max_sum_, max_indices_))

        # current player sum's updating:
        # sums[turn] += max_d_sum_
        # turn = (turn + 1) % 2
        # i_ = max_i_ + 1
    # winner's defining:
    print(f'{1 if sums[0] > sums[1] else 0}')


def get_max_data(start_index: int, end_index: int, numbers: list[int], is_max: bool = True):
    max_sum = -math.inf if is_max else math.inf
    max_indices = []
    sum_ = 0
    for i_ in range(start_index, end_index + 1):
        sum_ += numbers[i_]
        if is_max:
            if sum_ > max_sum:
                max_sum = sum_  # 36.6 98
        elif sum_ < max_sum:
            max_sum = sum_
        i_ += 1
    sum_ = 0
    for i_ in range(start_index, end_index + 1):
        sum_ += numbers[i_]
        if sum_ == max_sum:
            max_indices.append(i_)
        i_ += 1
    return max_sum, max_indices


def get_pars():
    n, m = map(int, input().split())
    numbers = [int(_) for _ in input().split()]
    return n, m, numbers


get_winner()
