import random


class Polynomial:
    digits_set = {'0', '1', '2', '3', '4', '5', '6', '7', '8', '9'}

    def __init__(self, pol_str: str):
        self.coefficients = {}
        self.get_coefficients_from_string(pol_str)
        print(f'self.coefficients: {self.coefficients}')

    @staticmethod
    def get_random_pol(max_power: int, max_abs_coeff: int):
        random_pol = Polynomial('')
        for i in range(max_power, -1, -1):
            if i == max_power:
                c = 0
                while c == 0:
                    c = random.randint(- max_abs_coeff, max_abs_coeff)
            else:
                c = random.randint(- max_abs_coeff, max_abs_coeff)
            random_pol.coefficients[i] = c
        random_pol.stabilize()
        print(f'pol_dict: {random_pol.coefficients}')
        return random_pol

    def get_coefficients_from_string(self, pol_str):
        if pol_str == '' or pol_str == '0':
            self.coefficients = {}
            return

        j = 0  # walking dead index

        while True:
            is_neg: bool = False
            num = 0
            power = 0

            if j < len(pol_str) and pol_str[j] == '-':
                is_neg = True
                j += 1

            while j < len(pol_str) and pol_str[j] in self.digits_set:
                num *= 10
                num += int(pol_str[j])
                j += 1

            if num == 0:
                num = 1

            if is_neg:
                num *= -1

            if j == len(pol_str):
                self.coefficients[0] = num
                break

            if pol_str[j] == 'x':
                j += 1

                if j < len(pol_str) and pol_str[j] == '^':
                    j += 1

                    while j < len(pol_str) and pol_str[j] in self.digits_set:
                        power *= 10
                        power += int(pol_str[j])
                        j += 1
                else:
                    power = 1

            self.coefficients[power] = num

            if j == len(pol_str) - 1 and pol_str[j] in self.digits_set:
                break

            if j < len(pol_str) and pol_str[j] == '+':
                j += 1

    def get_coefficients_from_file(self, file_path: str):
        self.coefficients = {}

        # operations with file
        with open(file_path, "r") as file:
            pol_str = file.readline()
            self.get_coefficients_from_string(pol_str)
            file.close()

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

    def multiply_by_num(self, multiple: int):
        result_pol = self.copy()
        for power_key in result_pol.coefficients:
            result_pol.coefficients[power_key] *= multiple
        result_pol.stabilize()
        return result_pol

    def multiply(self, pol_to_be_multiplied_by):
        product = Polynomial('')
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

    def copy(self):
        new_pol = Polynomial("")
        new_pol.coefficients = self.coefficients.copy()
        return new_pol

    def simplify(self):
        return self

    def equals(self, other):
        return self.coefficients == other.coefficients

    def __neg__(self):
        return self.multiply_by_num(-1)

    def __add__(self, other):
        if type(other) == int:
            return self.add(Polynomial(str(other)))
        return self.add(other)

    def __sub__(self, other):
        if type(other) == int:
            return self.subtract(Polynomial(str(other)))
        return self.subtract(other)

    def __mul__(self, other):
        if type(other) == int:
            return self.multiply_by_num(other)
        return self.multiply(other)

    def __pow__(self, power: int, modulo=None):
        return self.raise_to_power(power)

    def __str__(self):
        return self.to_string()

    def __repr__(self):
        return self.to_string()

    @classmethod
    def min_polynomial(cls, p, q):
        pass

    @classmethod
    def max_polynomial(cls, p, q):
        pass


p1, p2 = Polynomial('3x^4+5x^3-4x^2+x+1'), Polynomial('x+1')

