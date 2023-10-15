# accepted on codewars.com
import math


def get_min_base(number):
    for power in range(int(math.log2(number)), 1, -1):
        base = int(pow(number, 1 / power))
        rem = number
        while rem > 1 and (rem - 1) % base == 0:
            rem = (rem - 1) // base
        if rem == 1:
            return base
    return number - 1


# tests:
print(get_min_base(15707167547816771049468892261))  # 660
print(get_min_base(17068173672105403454090386))  # 111285


