from functools import reduce

from AmberCode.HWSem4.Fraction import Fraction
from AmberCode.HWSem4.Polynomial import Polynomial


class FractPol:

    def __init__(self, pol_str: str):
        self.coefficients = {}
        pol = Polynomial(pol_str)
        if len(pol.coefficients) != 0:
            for pol_power_key in pol.coefficients:
                self.coefficients[pol_power_key] = Fraction(pol.coefficients[pol_power_key])

    def to_string(self) -> str:
        pol_str = ''
        if len(self.coefficients) == 0:
            return '0'
        for power_key in self.coefficients:
            coeff = self.coefficients[power_key]  # cannot be equal to zero
            if power_key != max(self.coefficients.keys()):  # not for leading power
                pol_str += '+' if coeff > 0 else '-'
            else:
                pol_str += '-' if coeff < 0 else ''
            pol_str += str(abs(coeff)) if abs(coeff) != 1 else '' if power_key != 0 else '1'
            pol_str += 'x' if power_key != 0 else ''
            pol_str += '^' + str(power_key) if power_key > 1 else ''
        return pol_str

    def print(self):
        print(self.to_string())

    def stabilize(self):  # removes all zero-values (coeffs) and sort the dict in increasing order
        self.coefficients = {key: value for key, value in sorted(self.coefficients.items(), reverse=True) if value != 0}

    def add(self, pol_to_be_added):
        result_pol = self.copy()
        for power_key in pol_to_be_added.coefficients:
            if power_key in result_pol.coefficients:
                result_pol.coefficients[power_key] += pol_to_be_added.coefficients[power_key]
            else:
                result_pol.coefficients[power_key] = pol_to_be_added.coefficients[power_key]
        result_pol.stabilize()
        return result_pol

    def subtract(self, pol_to_be_subtracted):
        return self.add(-pol_to_be_subtracted)

    def multiply_by_num(self, multiple):
        result_pol = self.copy()
        for power_key in self.coefficients:
            result_pol.coefficients[power_key] *= multiple
        result_pol.stabilize()
        return result_pol

    def multiply(self, pol_to_be_multiplied_by):
        product = FractPol('')
        for left_power_key in self.coefficients:
            for right_power_key in pol_to_be_multiplied_by.coefficients:
                if left_power_key + right_power_key in product.coefficients:
                    product.coefficients[left_power_key + right_power_key] += self.coefficients[left_power_key] * pol_to_be_multiplied_by.coefficients[right_power_key]
                else:
                    product.coefficients[left_power_key + right_power_key] = self.coefficients[left_power_key] * pol_to_be_multiplied_by.coefficients[right_power_key]
        product.stabilize()
        return product

    def raise_to_power(self, power: int):
        return Polynomial.raise_to_power_aux(self.copy(), power)

    @staticmethod
    def raise_to_power_aux(pol_to_be_raised, power: int):
        if power < 0:
            print('Cannot be applied with power < 0, the polynomial stays the same')
            return pol_to_be_raised
        if power == 0:
            pol_to_be_raised.coefficients = {0: 1}
            return pol_to_be_raised
        if power == 1:
            return pol_to_be_raised
        if power % 2 == 0:
            return Polynomial.raise_to_power_aux(pol_to_be_raised.multiply(pol_to_be_raised), power // 2)
        else:
            return pol_to_be_raised.multiply(Polynomial.raise_to_power_aux(pol_to_be_raised.multiply(pol_to_be_raised), (power - 1) // 2))

    def polynomial_of_polynomial(self, pol_as_x):
        polynomial_of_polynomial = Polynomial('')
        for self_power_key in self.coefficients:
            curr_pol = pol_as_x.copy()
            curr_pol.raise_to_power(self_power_key)
            curr_pol.multiply_by_num(self.coefficients[self_power_key])
            polynomial_of_polynomial.add(curr_pol)
        polynomial_of_polynomial.stabilize()
        return polynomial_of_polynomial

    def rem(self, divisor):
        return self.remainder(divisor, True)

    def quotient(self, divisor):
        return self.remainder(divisor, False)

    def remainder(self, divisor, rem_or_quot: bool):
        if max(self.coefficients.keys()) < max(divisor.coefficients.keys()):
            return self.copy()

        quotient = FractPol('')
        remainder = self.copy()
        temporal_pol = FractPol('')

        while len(remainder.coefficients) > 0 and max(remainder.coefficients.keys()) >= max(divisor.coefficients.keys()):
            rem_max_power = max(remainder.coefficients.keys())  # 36 366 98 989
            divisor_max_power = max(divisor.coefficients.keys())

            coefficient = remainder.coefficients[rem_max_power] / divisor.coefficients[divisor_max_power]

            quotient.coefficients[rem_max_power - divisor_max_power] = coefficient

            temporal_pol = divisor.copy().multiply_by_num(coefficient)

            counter = divisor_max_power
            for j in range(rem_max_power, rem_max_power - divisor_max_power - 1, -1):
                if counter in temporal_pol.coefficients:
                    if j in remainder.coefficients:
                        remainder.coefficients[j] -= temporal_pol.coefficients[counter]
                    else:
                        remainder.coefficients[j] = -temporal_pol.coefficients[counter]
                counter -= 1

            remainder.stabilize()

        return remainder if rem_or_quot else quotient

    def max_pow(self):
        return -1 if len(self.coefficients) == 0 else max(self.coefficients.keys())

    def gcd(self, pol):
        p = self.copy()
        q = pol.copy()

        while p.max_pow() >= 1 and q.max_pow() >= 1:
            if p.max_pow() >= q.max_pow():
                p = p.rem(q)
            else:
                q = q.rem(p)

        if FractPol.min_polynomial(p, q) == FractPol('0'):
            return FractPol.max_polynomial(p, q).simplify()
        else:
            return FractPol.min_polynomial(p, q).simplify()

    def lcm(self, pol):
        return (self.multiply(pol)).quotient(self.gcd(pol))

    def value_at(self, coord):
        return reduce(lambda x, y: self.coefficients[y] * (coord ** y) + x, self.coefficients, 0) if len(self.coefficients) > 0 else 0

    @classmethod
    def min_polynomial(cls, pol1, pol2):
        return pol1 if pol1.max_pow() <= pol2.max_pow() else pol2

    @classmethod
    def max_polynomial(cls, pol1, pol2):
        return pol1 if pol1.max_pow() >= pol2.max_pow() else pol2

    def copy(self):
        new_pol = FractPol('')
        new_pol.coefficients = self.coefficients.copy()
        return new_pol

    def simplify(self):
        simplified_pol = self.copy()
        if len(simplified_pol.coefficients) > 0:
            if simplified_pol.coefficients[max(simplified_pol.coefficients.keys())] < 0:
                simplified_pol *= -1

        num_gcd = reduce(lambda x, y: Fraction.gcd(x, y.numerator), simplified_pol.coefficients.values(), 0)
        den_gcd = reduce(lambda x, y: Fraction.gcd(x, y.denominator), simplified_pol.coefficients.values(), 0)

        simplified_pol *= Fraction(den_gcd, num_gcd)
        return simplified_pol

    def minus(self):
        return self.multiply_by_num(-1)

    def equals(self, other):
        return self.coefficients == other.coefficients

    def __eq__(self, other):
        return self.equals(other)

    def __ne__(self, other):
        return not self.equals(other)

    def __neg__(self):
        return self.minus()

    def __add__(self, other):
        if type(other) == int:
            return self.add(Polynomial(str(other)))
        return self.add(other)

    def __sub__(self, other):
        if type(other) == int:
            return self.subtract(Polynomial(str(other)))
        return self.subtract(other)

    def __mul__(self, other):
        if type(other) == int or type(other) == Fraction:
            return self.multiply_by_num(other)
        return self.multiply(other)

    def __truediv__(self, other):
        return self.quotient(other)

    def __mod__(self, other):
        return self.rem(other)

    def __pow__(self, power: int, modulo=None):
        return self.raise_to_power(power)

    def __str__(self):
        return self.to_string()

    def __repr__(self):
        return self.to_string()


p1 = FractPol('x^3-1')
p2 = FractPol('x^2+x+1')

(p1.gcd(p2)).print()
(p1.lcm(p2)).print()

# p1.multiply_by_num(Fraction(-11, 1))
#
# print(p1.multiply_by_num(-1))
# print(p1.minus())
# print(p1 * p2)

print(p1)

print(p1.value_at(2))

print(FractPol('6x^2+6').simplify())
print(FractPol('x^2-1').gcd(FractPol('x^2+2x+1')))
print(FractPol('x^2-1').lcm(FractPol('x^2+2x+1')))

print(FractPol('x^2+19x-1') / FractPol('23x-111'))




