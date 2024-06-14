import math


class Vector:
    """Vector class"""

    def __init__(self, coords: list[int]):
        self.coords = tuple(coords)

    def equals(self, other: 'Vector'):

        if len(self.coords) != len(other.coords):
            return False

        return self.coords == other.coords

    def add(self, v: 'Vector') -> 'Vector':

        if len(self.coords) != len(v.coords):
            raise ValueError(f'Different dimensions vectors cannot be added to each other...')

        return Vector([v.coords[i] + self.coords[i] for i in range(len(self.coords))])

    def subtract(self, v: 'Vector') -> 'Vector':

        if len(self.coords) != len(v.coords):
            raise ValueError(f'Different dimensions vectors cannot be added to each other...')

        return Vector([self.coords[i] - v.coords[i] for i in range(len(self.coords))])

    def dot(self, v: 'Vector') -> int:

        if len(self.coords) != len(v.coords):
            raise ValueError(f'Different dimensions vectors cannot be added to each other...')

        return sum([v.coords[i] * self.coords[i] for i in range(len(self.coords))])

    def norm(self) -> float:
        return math.sqrt(sum([self.coords[i] ** 2 for i in range(len(self.coords))]))

    def __str__(self):
        k = ','.join([str(el) for el in self.coords])
        return f'({k})'

    def __repr__(self):
        return str(self)


# mask = [1, 2, 3]
#
#
# vector_a = Vector(mask)
#
# print(f'{vector_a.coords}')
#
# mask += [4]
#
# print(f'{vector_a.coords}')

a = Vector([1, 2, 3])
b = Vector([3, 4, 5])
c = Vector([5, 6, 7, 8])

print(f'{a.add(b)}')  # should return a new Vector([4, 6, 8])
print(f'{a.subtract(b)}')  # should return a new Vector([-2, -2, -2])
print(f'{a.dot(b)}')  # should return 1*3 + 2*4 + 3*5 = 26
print(f'{a.norm()}')  # should return sqrt(1^2 + 2^2 + 3^2) = sqrt(14)
print(f'{a.add(c)}')  # raises an exception
