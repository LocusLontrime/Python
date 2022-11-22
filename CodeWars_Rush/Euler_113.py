import time
import math
import operator as operator
from functools import reduce

from past.builtins import xrange

start = time.time()

# http://www.mathblog.dk/project-euler-113-googol-not-bouncy/


def combs(n, k):
    k = min(k, n - k)

    if k == 0:
        return 1

    numerator = reduce(operator.mul, xrange(n, n - k, -1))
    denominator = reduce(operator.mul, xrange(1, k + 1))

    return numerator // denominator


def insane_inc_or_dec(max_digits):
    return combs(max_digits + 10, 10) + combs(max_digits + 9, 9) - (10 * max_digits) - 2


elapsed = time.time() - start
print("%s found in %s seconds" % (insane_inc_or_dec(1000000), elapsed))

