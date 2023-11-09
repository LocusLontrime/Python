# accepted on codewars.com


def max_zero_sequence(arr):
    sum_ = 0
    dict_ = {0: [0]}
    best_range = None
    best_length = 0
    for i in range(len(arr)):
        sum_ += arr[i]
        if sum_ in dict_.keys():
            dict_[sum_].append(i + 1)
        else:
            dict_[sum_] = [i + 1]
    for k, v in dict_.items():
        l_ = v[-1] - v[0]
        if l_ > best_length:
            best_length = l_
            best_range = v[0], v[-1]
    res = arr[best_range[0]: best_range[1]]
    return res
