# accepted on codewars.com
import time
from fractions import Fraction


# memo table:
memo = {}
# rec counter:
rec_counter = 0


def equation(k: int) -> str:
    # memo table fulfilling:
    # if len(memo) == 0:
    #     equation_(145)
    print(f'k: {k}')
    return str(equation_(k))


def equation_(k: int) -> 'Polynomial':
    global rec_counter
    rec_counter += 1
    # wrong cases:
    if k < 0:
        print(f'k should be greater than 1')
        return Polynomial([])
    # base cases:
    if k == 0:
        return Polynomial([1, 0])
    if k not in memo.keys():
        # recursive equation's compounding:
        res_pol = Polynomial([])
        aux_pol = equation_(k - 1)
        res_pol += aux_pol.multiply(Polynomial([1, 0]))
        k_min_1_pol = aux_pol.polynomial_of_polynomial(Polynomial([1, -1]))
        # working with max power coeff:
        multiplier = 1 + k_min_1_pol.coefficients[max_key_ := max(k_min_1_pol.coefficients.keys())]
        del k_min_1_pol.coefficients[max_key_]
        for power_, val_ in k_min_1_pol.coefficients.items():
            res_pol -= equation_(power_).multiply_by_num(val_)
        # returning result:
        memo[k] = res_pol.multiply_by_num(Fraction(1) / multiplier)
    return memo[k]


class Polynomial:
    def __init__(self, coeffs: list[Fraction | int]):
        self.coefficients = {}
        for i, coeff in enumerate(coeffs):
            self.coefficients[len(coeffs) - i - 1] = coeff

    def to_string(self) -> str:
        pol_str = ''
        if len(self.coefficients) == 0:
            return '0'
        for power_key in self.coefficients:
            coeff = self.coefficients[power_key]  # cannot be equal to zero
            if power_key != max(self.coefficients.keys()):  # not for leading power
                pol_str += ' + ' if coeff > 0 else ' - '
            else:
                pol_str += ' - ' if coeff < 0 else ''
            pol_str += str(abs(coeff)) if abs(coeff) != 1 else '' if power_key != 0 else '1'
            pol_str += 'n' if power_key != 0 else ''
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

    def multiply_by_num(self, multiple: int):
        result_pol = self.copy()
        for power_key in result_pol.coefficients:
            result_pol.coefficients[power_key] *= multiple
        result_pol.stabilize()
        return result_pol

    def multiply(self, pol_to_be_multiplied_by):
        product = Polynomial([])
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
        polynomial_of_polynomial = Polynomial([])
        for self_power_key in self.coefficients:
            curr_pol = pol_as_x.copy()
            polynomial_of_polynomial += curr_pol.raise_to_power(self_power_key).multiply_by_num(self.coefficients[self_power_key])
        polynomial_of_polynomial.stabilize()
        return polynomial_of_polynomial

    def copy(self):
        new_pol = Polynomial([])
        new_pol.coefficients = self.coefficients.copy()
        return new_pol

    def simplify(self):
        return self

    def equals(self, other):
        return self.coefficients == other.coefficients

    def __neg__(self):
        return self.multiply_by_num(-1)

    def __add__(self, other):
        return self.add(other)

    def __sub__(self, other):
        return self.subtract(other)

    def __mul__(self, other):
        if type(other) == int:
            return self.multiply_by_num(other)
        return self.multiply(other)

    def __str__(self):
        return self.to_string()

    def __repr__(self):
        return self.to_string()


# pol = Polynomial([2, 5, 1, Fraction(2, 7)])
# pol_ = Polynomial([3, 2, 2, 98])
# print(f'pol: {pol}')
# print(f'pol: {pol_}')
# pol_sum = pol + pol_
# print(f'pol_sum: {pol_sum}')
# print(f'fraction: {Fraction(100, 3)}')

# print(f'{Fraction(1) / Fraction(3, 2)}')

start = time.time_ns()
eq = equation(98)
finish = time.time_ns()
print(f'eq: {eq}')
print(f'rec counter: {rec_counter}')
print(f'time elapsed: {(finish - start) // 10 ** 6} milliseconds')

# pol1 = Polynomial([1, 2])
# pol2 = Polynomial([1, 2, 3])
# print(f'pol: {pol1.polynomial_of_polynomial(pol2)}')
