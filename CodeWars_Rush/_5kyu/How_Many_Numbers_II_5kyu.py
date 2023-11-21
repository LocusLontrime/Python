# accepted on codewars.com
THRESHOLD = 1_000


def max_sum_dig(n_max: int, max_sum: int):
    right_numbers = []
    sum_ = 0
    for n in range(THRESHOLD, n_max + 1):
        n_str = f'{n}'
        flag = True
        for i in range((len(n_str) - 4) + 1):
            if sum(map(int, n_str[i: i + 4])) > max_sum:
                flag = False
                break
        if flag:
            right_numbers.append(n)
            sum_ += n
    print(f'{len(right_numbers)} right_numbers: {right_numbers}')
    print(f'sum_: {sum_}')
    mean_val = sum_ / len(right_numbers)
    print(f'mean_val: {mean_val}')
    mean_nearest_n = min(right_numbers, key=lambda x: (abs(x - mean_val), x))
    print(f'mean_nearest_n: {mean_nearest_n}')


max_sum_dig(82426, 9)
