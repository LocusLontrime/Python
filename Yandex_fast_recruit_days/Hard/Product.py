# accepted on coderun:
import sys


def product():
    # bottom-up dp-implementation:
    n, m, k, a = get_pars()

    # if a zero is in the array given:
    if m == 0:
        zero_index = a.index(0)
        the_path = [zero_index]
        ind_, counter = 0, 0
        while counter < k - 1:
            if ind_ != zero_index:
                the_path.append(ind_)
                counter += 1
            ind_ += 1
        return ' '.join([str(_ + 1) for _ in the_path])

    # 1s counting:
    ones = []  # 1s' indices...
    for i_, el_ in enumerate(a):
        if el_ == 1:
            ones.append(i_)
    # 1s quantity:
    ones_q = len(ones)

    # the end of paths:
    factors = [{1: None}]
    # null-filling:
    for _ in range(k):
        factors.append({})
    # the core bottom-up algo:
    for j in range(n):
        el_ = a[j]
        for i in range(k, 0, -1):
            for factor, path in factors[i - 1].items():
                if el_ not in [0, 1] and m % (el_ * factor) == 0:
                    factors[i][el_ * factor] = [j, path]
                    if k - ones_q <= i <= k and el_ * factor == m:
                        return recover_path(factors[i], m, ones, ones_q, k - i, k)
    return recover_path(factors[k], m, ones, ones_q, 0, k)


def recover_path(products_, m: int, ones: list[int], ones_q: int, ones_needed_q: int, k: int):
    # The final path is now contained in products_[m]:
    if m in products_.keys():
        nested_reversed_path = products_[m]
    else:
        nested_reversed_path = None
        ones_needed_q = k
    # path recovering:
    the_path = []
    while nested_reversed_path is not None:
        the_path.append(nested_reversed_path[0])
        nested_reversed_path = nested_reversed_path[1]
    # 1s appending:
    counter = 0
    for one in ones:
        if counter == ones_needed_q:
            break
        elif one not in the_path:
            the_path.append(one)
            counter += 1
    # re-indexing:
    return ' '.join([str(ind_ + 1) for ind_ in the_path])


def get_pars() -> tuple[int, int, int, list[int]]:
    n, m, k = [int(_) for _ in input().split(' ')]
    a = [int(_) for _ in input().split(' ')]
    return n, m, k, a


def main():
    print(product())


if __name__ == '__main__':
    main()




