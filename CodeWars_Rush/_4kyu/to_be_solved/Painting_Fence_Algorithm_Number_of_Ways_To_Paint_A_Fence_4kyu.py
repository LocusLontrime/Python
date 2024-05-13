import sys

sys.setrecursionlimit(10_000)


MODULO = 1000000007


def ways(n, k):                                                                                        # 36 366 98 989 98989 LL 
    # base cases:
    if k == 0:
        return 0
    if n == 2:
        return k * k
    if n == 1:
        return k
    # body of rec:
    # recurrent relation:
    return ((k - 1) * (ways(n - 1, k) + ways(n - 2, k))) % MODULO


print(f'res: {ways(4, 5)}')  # 580
# print(f'res: {ways(8638433, 9944756)}')  # 895647343
