# accepted on codewars.com
import math


def cycle(n):
    if math.gcd(10, n) > 1:
        return -1
    curr_val, iterator = 1, 0
    while True:
        iterator += 1
        curr_val = (curr_val * 10) % n
        if curr_val == 1:
            break
    return iterator


print(cycle(7))
