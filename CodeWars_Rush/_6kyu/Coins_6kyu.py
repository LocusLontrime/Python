# accepted on codewars.com
import math


def coins(coin1, coin2):

    if math.gcd(coin1, coin2) > 1:
        return -1

    set_of_sums = set()
    for i in range(0, coin2 + 1):
        for j in range(0, coin1 + 1):
            curr_sum = coin1 * i + coin2 * j
            if curr_sum <= coin1 * coin2:
                set_of_sums.add(curr_sum)

    set_all_elems = set(i for i in range(0, coin1 * coin2 + 1))

    print(set_all_elems)
    print(set_of_sums)

    print(set_all_elems - set_of_sums)

    return max(set_all_elems - set_of_sums)


# print(coins(90, 55))
# print(coins(968, 801))
print(coins(3, 5))
