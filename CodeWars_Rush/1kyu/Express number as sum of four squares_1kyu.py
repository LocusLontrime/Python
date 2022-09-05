# accepted on codewars.com
import math
import random
import time
from functools import reduce
from typing import Tuple

MR_THRESHOLD = 1  # only one Miller-Rabin check
FACTORIZATION_THRESHOLD = 3  # (only 3, 5, 7)


# checks if the remainder can be expressed by the sum of three squares
def check_three_sqrs_repr(remainder: int) -> int:
    while remainder % 4 == 0:
        remainder //= 4
    return remainder % 8 != 7


# the main method
def four_squares(n: int) -> Tuple[int, int, int, int]:
    if n in [0, 1]:
        return [(0, 0, 0, 0), (1, 0, 0, 0)][n]
    if check_three_sqrs_repr(n):
        # three squares representation
        print(f'three squares representation')
        f_sq, s_sq, factors = find_good_sq(n)
    else:
        # four squares representation
        print(f'four squares representation')
        f_sq, s_sq, factors = find_two_good_squares(n)
    common_prod = reduce(lambda y, x: y * (x ** factors[x] if x < 8 else 1), factors.keys(), 1)  # 8 depends on FACTORIZATION_THRESHOLD, it is equal to the max_prime + 1
    largest_prime = max(factors.keys())
    print(f'common_prod: {common_prod}, largest_prime: {largest_prime}')
    print(f'now squarifying the common_prod and the largest_prime')
    t_sq, fourth_sq = squarify_little_number(common_prod) if largest_prime < 8 else unify_squares(squarify_little_number(common_prod), squarify_prime(largest_prime))
    print(f'been squarified, the result obtained:')
    return f_sq, abs(s_sq), abs(t_sq), abs(fourth_sq)


# for the cases like rem = 2 * 5 * (big prime of a kind 4k + 1), we squarify the product of 2 and 5
def squarify_little_number(number: int) -> Tuple[int, int]:
    print(f'squarifying of little number: {number}')
    f_sq = math.isqrt(number)
    while (s_sq := math.isqrt(rem := number - f_sq ** 2)) ** 2 != rem:
        f_sq -= 1
    print(f'the number been squarified: {number} = {f_sq}^2 + {s_sq}^2')
    return f_sq, s_sq


# checks if the remainder can be expressed by the sum of two squares, here we are searching for quasi-primes: 2 * 5 * (big prime of a kind 4k + 1) etc
def check_two_sqrs_repr(remainder: int) -> dict[int, int]:
    print(f'checking two squares representation... current remainder: {remainder}')
    factors = dict()
    power_counter = 0
    factor_counter = 0
    while remainder % 2 == 0:
        remainder //= 2
        power_counter += 1
    if power_counter >= 1:
        factors[2] = power_counter
    if is_prime(remainder):
        if remainder % 4 != 3:
            factors[remainder] = 1
            return factors
        else:
            return {}
    i = 2 + 1
    while i < int(math.sqrt(remainder)):
        if is_prime(i):
            factor_counter += 1
            if factor_counter > FACTORIZATION_THRESHOLD:
                return {}
            power_counter = 0
            while remainder % i == 0:
                remainder //= i
                power_counter += 1
            if i % 4 == 3 and power_counter % 2 == 1:
                return {}
            if power_counter >= 1:
                factors[i] = power_counter
            if is_prime(remainder):
                if remainder % 4 != 3:
                    factors[remainder] = 1
                    break
                else:
                    return {}
        i += 2
    return factors


# simplify the product of two pairs of squares into one pair of them
def unify_squares(squares1: tuple[int, int], squares2: tuple[int, int]) -> tuple[int, int]:
    return squares1[0] * squares2[0] + squares1[1] * squares2[1], squares1[0] * squares2[1] - squares1[1] * squares2[0]


# finds the first valid square
def find_good_sq(number: int) -> (int, int, dict[int, int]):
    f_sq = math.isqrt(number)
    while True:
        rem = number - f_sq ** 2
        if factors := check_two_sqrs_repr(rem):  # is_prime(rem):
            print(f'factors: {factors}')
            return f_sq, 0, factors  # s_sq = 0
        print(f'square: {f_sq}')
        f_sq -= 1


# finds the first and second valid squares
def find_two_good_squares(number: int) -> (int, int, dict[int, int]):
    f_sq = math.isqrt(number)
    print(f'now trying to found a valid f_sq one so that the rem can be expressed by the sum of three squares')
    while not check_three_sqrs_repr(rem := number - f_sq ** 2):
        print(f'f_sq: {f_sq}')
        f_sq -= 1
    s_sq, factors = (arr := find_good_sq(rem))[0], arr[2]
    return f_sq, s_sq, factors


# Miller-Rabin prime test section
def get_pars(n):
    power, multiplier = 0, n
    while multiplier % 2 == 0:
        power += 1
        multiplier >>= 1
    return power, multiplier


def miller_rabin_test(a, p):
    power, multiplier = get_pars(p - 1)
    a = pow(a, multiplier, p)
    if a == 1:
        return True
    for i in range(power):
        if a == p - 1:
            return True
        a = pow(a, 2, p)
    return False


def is_prime(p):
    if p == 2:
        return True
    if p <= 1 or p % 2 == 0:
        return False
    return all(miller_rabin_test(random.randint(2, p - 1), p) for _ in range(MR_THRESHOLD))


# prime squarifying section, implementation from Robin Chapman (stackoverflow):
def mods(a, n):
    if n <= 0:
        return "negative modulus"
    a = a % n
    if 2 * a > n:
        a -= n
    return a


def powmods(a, r, n):
    out = 1
    while r > 0:
        if (r % 2) == 1:
            r -= 1
            out = mods(out * a, n)
        r //= 2
        a = mods(a * a, n)
    return out


def quos(a, n):
    if n <= 0:
        return "negative modulus"
    return (a - mods(a, n)) // n


# remainder in Gaussian integers when dividing w by z
def gaussian_rem(w, z):
    (w0, w1) = w
    (z0, z1) = z
    n = z0 * z0 + z1 * z1
    if n == 0:
        return "division by zero"
    u0 = quos(w0 * z0 + w1 * z1, n)
    u1 = quos(w1 * z0 - w0 * z1, n)
    return (w0 - z0 * u0 + z1 * u1,
            w1 - z0 * u1 - z1 * u0)


def ggcd(w, z):
    while z != (0, 0):
        w, z = z, gaussian_rem(w, z)
    return w


def root4(p):
    # 4th root of 1 modulo p
    if (p % 4) != 1:
        return "not congruent to 1"

    k = p // 4
    j = 2

    while True:
        a = powmods(j, k, p)
        b = mods(a * a, p)
        if b == -1:
            return a
        if b != 1:
            return "not prime"
        j += 1


def squarify_prime(p):
    a = root4(p)
    return ggcd((p, 0), (a, 1))


start = time.time_ns()
# print(four_squares(242737486475111359018937623004230274909))
# print(four_squares(26346576505626211071173092937238937395))
# print(four_squares(197721028769447061884901744969553607124))
# print(four_squares(193086069356689959949887997745786088980))
# print(four_squares(97302902939768944330281642066698899076))
# print(four_squares(25649756661700011813625652281997236200))
# print(four_squares(335933872382306604464270151609014879498))
# print(four_squares(135646225796685104246753655845310331070))
# print(four_squares(331394253791585650918419425662905328681))
# print(four_squares(131028697213882621750665454396023141952))
# print(four_squares(151288305176950366782204607001869726443))
# print(four_squares(280277518346247092277148242865824612237))
# print(four_squares(75195738115238615831591408954880515868))
# print(four_squares(329316809761143348295830191349385194914))
# print(four_squares(183206635342628982622201830752599921468))
# print(four_squares(299905899944097775267809237958174129484))
# print(four_squares(50309263556368412816186911060720860018))
# print(four_squares(182515309002241768995801194677822322408))
# print(four_squares(45222385181005901571090851522393468233))
# print(four_squares(221156890975709486023061484450459449553))
# print(four_squares(32121157751893128165713514977432626239))
print(four_squares(18385753113772583909926064141947127021691434720742756438176823408496019300590278743917444455575688890503864624753348597547657772047567830556309613373433644444428010807386742762594687116986153336557212350465852569199503113953433721119901604756727665155633537447975368261091579496834837896851657542959286456943))
# print(four_squares(118071749310504676627289622665894446310329740459744331130706991159539243234182645291148193468553495059535818857677687809801028626305628173366631727109825593397621109369489642190087989326522034384363449057292037505157731945972507546015180590595898640762706434905693582777395777974398435530453929823854319937804))
# print(check_three_sqrs_repr(63089093323171555876383459807541911336583611265623947526173954206025134026575604313200971734959034006401850080479661367162840591836001399607885899386457761031815541644988267590513422814522128041084706209996499223062920615573796350735896335957297991551402634338080606054812973937135932246408363296677903292265))
# print(four_squares(63089093323171555876383459807541911336583611265623947526173954206025134026575604313200971734959034006401850080479661367162840591836001399607885899386457761031815541644988267590513422814522128041084706209996499223062920615573796350735896335957297991551402634338080606054812973937135932246408363296677903292265))
# print(four_squares(215))
finish = time.time_ns()

print(f'Time elapsed: {(finish - start) // 10 ** 6} milliseconds')
