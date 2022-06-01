import math


def get_nth_reverse_num(index: int) -> int:  # accepted on codewars.com
    L = int(math.log10(index))
    flag = 1 < index < 1.1 * (10 ** L)
    P = 10 ** (L - (1 if flag else 0))
    index -= P
    list_of_digs = list(str(index // (10 if index >= P else 1)))
    list_of_digs.reverse()
    return index * (10 ** (L - (1 if flag else 0))) + int("".join(list_of_digs))


print(get_nth_reverse_num(2345))


