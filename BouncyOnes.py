import math


def total_inc_dec(power_of_ten):
    return math.comb(power_of_ten + 9, 9) + math.comb(power_of_ten + 10, 10) - 10 * power_of_ten - 1


print(total_inc_dec(6))

