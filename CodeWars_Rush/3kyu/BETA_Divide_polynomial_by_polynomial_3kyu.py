# accepted on codewars.com
import re


def divide(P1, P2):  # LL 36 366 98 989
    print(f'p1: {P1}, p2: {P2}')
    q, r = divmod(Polynomial(P1), Polynomial(P2))
    return [str(q), int(str(r))]


class Polynomial:
    # decimal number system:
    BASE = 10

    def __init__(self, pol_str: str) -> None:
        self.coefficients = {}
        self.get_coefficients_from_string(pol_str)

    def get_coefficients_from_string(self, pol_str: str) -> None:
        coeffs = re.split('[+|-]', pol_str)
        index = 0

        if coeffs[0] == '':
            coeffs.remove(coeffs[0])
            index += 1

        max_p = len(coeffs) - 1

        for i, coeff in enumerate(coeffs):
            multiplier = 1
            if pol_str[index - 1] == '-':
                multiplier = -1
            if coeff[0].isdigit():
                ind = 0
                coeff_ = 0
                while ind < len(coeff) and (c := coeff[ind]).isdigit():
                    coeff_ = coeff_ * self.BASE + int(c)
                    ind += 1
                self.coefficients[max_p - i] = coeff_ * multiplier
            else:
                self.coefficients[max_p - i] = multiplier
            index += len(coeff) + 1

    def multiply_by_num(self, multiple):
        result_pol = self.copy()
        for power_key in self.coefficients:
            result_pol.coefficients[power_key] *= multiple
        result_pol.stabilize()
        return result_pol

    # removes all zero-values (coeffs) and sort the dict in increasing order
    def stabilize(self):
        self.coefficients = {key: value for key, value in sorted(self.coefficients.items(), reverse=True) if value != 0}

    def divide(self, divisor: 'Polynomial') -> tuple['Polynomial', 'Polynomial']:
        quotient = Polynomial('0')
        remainder = self.copy()

        while len(remainder) > 0 and (rem_max_power := max(remainder.coefficients.keys())) >= len(divisor) - 1:
            divisor_max_power = len(divisor) - 1
            if rem_max_power in remainder.coefficients.keys():
                coefficient = remainder.coefficients[rem_max_power]

            quotient.coefficients[rem_max_power - divisor_max_power] = coefficient
            temporal_pol = divisor.copy().multiply_by_num(coefficient)

            for i in range(l := len(divisor)):
                key = rem_max_power - i
                if l - 1 - i in temporal_pol.coefficients.keys():
                    if key in remainder.coefficients.keys():
                        remainder.coefficients[key] -= temporal_pol.coefficients[l - 1 - i]
                    else:
                        remainder.coefficients[key] = -temporal_pol.coefficients[l - 1 - i]

            remainder.stabilize()

        return quotient, remainder

    def copy(self) -> 'Polynomial':
        new_pol = Polynomial('0')
        new_pol.coefficients = self.coefficients.copy()
        return new_pol

    def __len__(self) -> int:
        return len(self.coefficients)

    def __str__(self) -> str:
        pol_str = ''
        if len(self.coefficients) == 0:
            return '0'
        for power_key in list(sorted(self.coefficients.keys(), key=lambda x: -x)):
            coeff = self.coefficients[power_key]  # cannot be equal to zero
            if power_key != max(self.coefficients.keys()):  # not for leading power
                pol_str += '+' if coeff > 0 else '-'
            else:
                pol_str += '-' if coeff < 0 else ''
            pol_str += str(abs(coeff)) if abs(coeff) != 1 else '' if power_key != 0 else '1'
            pol_str += 'x' if power_key != 0 else ''
            pol_str += '**' + str(power_key) if power_key > 1 else ''
        return pol_str

    def __repr__(self):
        return str(self)

    def __divmod__(self, other: 'Polynomial') -> tuple['Polynomial', 'Polynomial']:
        return self.divide(other)


# p1, p2 = Polynomial('2x**4+5x**3-4x**2+x+1'), Polynomial('x+1')
# p1_, p2_ = Polynomial('x**3-4x**2+3x+11'), Polynomial('x+3')
# r_, q_ = p1.divide(p2)
# print(f'r coeffs: {r_.coefficients}, q coeffs: {q_.coefficients}')
# print(f'p1 / p2: {r_, q_}')
# r_, q_ = p1_.divide(p2_)
# print(f'r coeffs: {r_.coefficients}, q coeffs: {q_.coefficients}')
# print(f'p1 / p2: {r_, q_}')

p1, p2 = Polynomial('-989x**4-36x**3+98x**2+98989x-98'), Polynomial('x+98')
r_, q_ = p1.divide(p2)
print(f'r coeffs: {r_.coefficients}, q coeffs: {q_.coefficients}')
print(f'p1 / p2: {r_, q_}')

