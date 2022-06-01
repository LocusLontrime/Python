class Fraction:

    def __init__(self, numerator: int, denominator=1):  # common constructor
        if denominator != 0:
            self.numerator = numerator
            self.denominator = denominator
            self.is_integer = False
            self.simplify()
        else:
            print('Denominator cannot be equal to Zero!')  # what to do with fraction's fields?

    def simplify(self):  # simplifying the fraction
        if self.numerator == 0 and self.denominator != 0:
            self.denominator = 1
            self.is_integer = True
            return

        if self.denominator < 0:
            print('Denominator is less than Zero, it equals ' + str(self.denominator))
            return

        is_less_than_zero = self.numerator < 0
        if is_less_than_zero:
            self.numerator *= -1

        if self.numerator != 0 and self.denominator % self.numerator == 0:
            self.denominator //= self.numerator
            self.numerator = 1

        elif self.numerator % self.denominator == 0:
            self.numerator //= self.denominator
            self.denominator = 1
            self.is_integer = True

        else:
            gcd = Fraction.gcd(self.numerator, self.denominator)
            self.numerator //= gcd
            self.denominator //= gcd

        if is_less_than_zero:
            self.numerator *= -1

    def equals(self, fraction) -> bool:
        return self.numerator * fraction.denominator == self.denominator * fraction.numerator

    def is_more(self, fraction):
        return self.numerator * fraction.denominator > self.denominator * fraction.numerator

    @staticmethod
    def max_fraction(fraction_1, fraction_2):
        return fraction_2 if (fraction_2.is_more(fraction_1)) else fraction_1

    @staticmethod
    def min_fraction(fraction_2, fraction_1):
        return fraction_2 if (fraction_2.is_more(fraction_1)) else fraction_1

    @staticmethod
    def gcd(a: int, b: int) -> int:  # euclidean_algorithm, finds the GCD of two nums (numerator and denominator)
        while a != 0 and b != 0:
            if a > b:
                a %= b
            else:
                b %= a
        return a + b

    def minus(self):
        return Fraction(-self.numerator, self.denominator)

    def inverse(self):
        if self.numerator == 0:
            print("The fraction cannot be inverted, since its numerator is equal to zero")
            return self.copy()

        if self.numerator < 0:
            return Fraction(-self.denominator, -self.numerator)
        else:
            return Fraction(self.denominator, self.numerator)

    def add(self, fraction_to_be_added):
        return Fraction(self.numerator * fraction_to_be_added.denominator +
                        self.denominator * fraction_to_be_added.numerator, self.denominator * fraction_to_be_added.denominator)

    def subtract(self, fraction_to_be_subtracted):
        return Fraction(self.numerator * fraction_to_be_subtracted.denominator -
                        self.denominator * fraction_to_be_subtracted.numerator, self.denominator * fraction_to_be_subtracted.denominator)

    def multiply(self, fraction_multiplier):
        return Fraction(self.numerator * fraction_multiplier.numerator, self.denominator * fraction_multiplier.denominator)

    def divide(self, fraction_divisor):
        if fraction_divisor.numerator == 0:
            print("Cannot be divided by Zero")
        if self.denominator * fraction_divisor.numerator > 0:
            return Fraction(self.numerator * fraction_divisor.denominator, self.denominator * fraction_divisor.numerator)
        else:
            return Fraction(-self.numerator * fraction_divisor.denominator, -self.denominator * fraction_divisor.numerator)

    def raise_to_power(self, power: int):
        return Fraction.raise_to_power_aux(self.copy(), power)

    @staticmethod
    def raise_to_power_aux(fraction, power: int):
        if power == 0:
            return Fraction(1)
        if power == 1:
            return fraction

        if power % 2 == 0:
            return Fraction.raise_to_power_aux(fraction.multiply(fraction), power // 2)
        else:
            return fraction.multiply(Fraction.raise_to_power_aux(fraction.multiply(fraction), (power - 1) // 2))

    def to_string(self):
        fractions_str = ''
        is_negative = self.numerator < 0
        if is_negative:
            self.numerator *= -1
        if self.denominator != 0:
            n = self.numerator // self.denominator
            if self.numerator > self.denominator:
                if self.is_integer:
                    if is_negative:
                        fractions_str += str(-n)
                    else:
                        fractions_str += str(n)
                else:
                    if is_negative:
                        fractions_str += str(-n) + '(' + str(self.numerator - n * self.denominator) + '/' + str(self.denominator) + ')'
                    else:
                        fractions_str += str(n) + '(' + str(self.numerator - n * self.denominator) + '/' + str(self.denominator) + ')'
            elif self.numerator == self.denominator:
                if is_negative:
                    fractions_str += '-1'
                else:
                    fractions_str += '1'
            else:
                if self.is_integer:
                    fractions_str += '0'
                else:
                    if is_negative:
                        fractions_str += str(-self.numerator) + '/' + str(self.denominator)
                    else:
                        fractions_str += str(self.numerator) + '/' + str(self.denominator)
        else:
            print("Denominator cannot be equal to Zero, fraction does not exist!")
        if is_negative:
            self.numerator = -self.numerator
        return fractions_str

    def copy(self):
        return Fraction(self.numerator, self.denominator)

    def print(self):
        print(self.to_string())

    def __eq__(self, other):
        if type(other) == int:
            other = Fraction(other)
        return self.equals(other)

    def __ne__(self, other):
        if type(other) == int:
            other = Fraction(other)
        return not self.equals(other)

    def __neg__(self):
        return self.minus()

    def __lt__(self, other):
        if type(other) == int:
            other = Fraction(other)
        return not self.is_more(other)

    def __gt__(self, other):
        if type(other) == int:
            other = Fraction(other)
        return self.is_more(other)

    def __le__(self, other):
        if type(other) == int:
            other = Fraction(other)
        return not self.is_more(other) or self.equals(other)

    def __ge__(self, other):
        if type(other) == int:
            other = Fraction(other)
        return self.is_more(other) or self.equals(other)

    def __add__(self, other):
        if type(other) == int:
            other = Fraction(other)
        return self.add(other)

    def __sub__(self, other):
        if type(other) == int:
            other = Fraction(other)
        return self.subtract(other)

    def __mul__(self, other):
        if type(other) == int:
            other = Fraction(other)
        return self.multiply(other)

    def __truediv__(self, other):
        if type(other) == int:
            other = Fraction(other)
        return self.divide(other)

    def __pow__(self, power: int, modulo=None):
        return self.raise_to_power(power)

    def __abs__(self):
        return Fraction(abs(self.numerator), self.denominator)

    def __str__(self):
        return self.to_string()

    def __repr__(self):
        return self.to_string()


