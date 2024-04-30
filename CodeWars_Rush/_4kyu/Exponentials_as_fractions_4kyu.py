# accepted on codewars.com
from fractions import Fraction


def expand(x: float, digit: int):
    e_approx = monomial = power = 1
    while len(str(e_approx.numerator)) < digit:
        # adding a new Taylor series monomial:
        monomial *= Fraction(10 * x) / (10 * power)
        e_approx += monomial
        power += 1
    return [e_approx.numerator, e_approx.denominator]


# expand(2, 5)  # --> [20947, 2835]

# expand(3, 10)  # --> [7205850259, 358758400]

# expand(1.5, 10)  # --> [36185315027,8074035200]

expand(1.6, 10)  # --> [27425286391, 5537109375]

print(f'{Fraction(1.6)}')
