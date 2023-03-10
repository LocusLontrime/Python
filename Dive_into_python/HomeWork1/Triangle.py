# Task 1.
# Треугольник существует только тогда, когда сумма любых двух его сторон больше третьей.
# Дано a, b, c - стороны предполагаемого треугольника. Требуется сравнить длину каждого отрезка-стороны с суммой двух других.
# Если хотя бы в одном случае отрезок окажется больше суммы двух других, то треугольника с такими сторонами не существует.
# Отдельно сообщить является ли треугольник разносторонним, равнобедренным или равносторонним.


import math


class Triangle:
    """represents a Triangle if such exists"""
    types = ['right', 'isosceles', 'equilateral']
    PRECISION = 5

    def __init__(self, a: int | float, b: int | float, c: int | float) -> None:
        self._a, self._b, self._c = a, b, c
        # check:
        if ch := self.check():
            raise ValueError(f'No triangle can have sides given: a: {self.a}, b: {self.b}, c:{self.c}, coz {ch}')

    @property
    def a(self):
        return round(self._a, self.PRECISION)

    @property
    def b(self):
        return round(self._b, self.PRECISION)

    @property
    def c(self):
        return round(self._c, self.PRECISION)

    @property
    def type(self) -> str | list[str]:
        """return the type of triangle"""
        triangle_type = []
        # if triangle is right (PRECISION par used):
        prec = 10 ** (-self.PRECISION)
        if abs(self._a ** 2 + self._b ** 2 - self._c ** 2) <= prec or\
                abs(self._a ** 2 + self._c ** 2 - self._b ** 2) <= prec or \
                abs(self._b ** 2 + self._c ** 2 - self._a ** 2) <= prec:
            triangle_type.append(self.types[0])
        # if triangle is equilateral:
        if self.a == self.b == self.c:
            triangle_type.append(self.types[2])
        elif len({self.a, self.b, self.c}) == 2:
            triangle_type.append(self.types[1])
        return triangle_type or ['scalene']

    def check(self) -> str:
        """checks if triangle can have the sides given (a, b, c)"""
        error_text = None
        if self.a + self.b <= self.c:
            error_text = f'{self.a} + {self.b} <= {self.c}'
        elif self.a + self.c <= self.b:
            error_text = f'{self.a} + {self.c} <= {self.b}'
        elif self.b + self.c <= self.a:
            error_text = f'{self.b} + {self.c} <= {self.a}'
        return error_text

    def __str__(self):
        return f'a: {self.a}, b: {self.b}, c: {self.c}, type: {", ".join(self.type)}'

    def __repr__(self):
        return str(self)


tr1 = Triangle(2, 2, 2 * math.sqrt(2))
print(f'tr -> {tr1}')

tr2 = Triangle(3, 4, 5)
print(f'tr -> {tr2}')

tr3 = Triangle(98, 98, 98)
print(f'tr -> {tr3}')

tr4 = Triangle(3, 4, 98)
print(f'tr -> {tr4}')



