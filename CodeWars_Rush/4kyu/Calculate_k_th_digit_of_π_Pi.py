import math


# using the Simon Plouffe 1995y method
def pi(k):
    pass


def calc_inner_sum(precision: int, iteration: int):
    increased_precision = precision + 5
    return round(4 / (8 * iteration + 1) - 2 / (8 * iteration + 4) - 1 / (8 * iteration + 5) - 1 / (8 * iteration + 6), increased_precision)


