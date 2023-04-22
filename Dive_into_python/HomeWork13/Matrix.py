from Dive_into_python.HomeWork13 import Exceptions


class Matrix:
    """represents a rectangular matrix"""
    def __init__(self, matrix: list[list[int]]):
        set_ = set()
        for row in matrix:
            set_.add(len(row))
            if len(set_) > 1:
                raise Exceptions.ShapeMatrixError(f"Matrix' rows must have the same lengths!")
        self.matrix = matrix

    def check_sizes(self, other: 'Matrix'):
        return len(self.matrix) == len(other.matrix) and len(self.matrix[0]) == len(other.matrix[0])

    def core(self, other: 'Matrix', sign_plus: bool = True):
        if not self.check_sizes(other):
            raise Exceptions.MatrixAdditionSubtractionError(f'Matrices must have the same sizes!')
        return Matrix([[self.matrix[j][i] + (1 if sign_plus else - 1) * other.matrix[j][i] for i in range(len(self.matrix[0]))] for j in
                       range(len(self.matrix))])

    def __add__(self, other: 'Matrix'):
        return self.core(other)

    def __sub__(self, other: 'Matrix'):
        return self.core(other, False)

    def __eq__(self, other: 'Matrix'):
        if not self.check_sizes(other):
            return False
        for j, row in enumerate(self.matrix):
            for i, el in enumerate(row):
                if el != other.matrix[j][i]:
                    return False
        return True

    def __ne__(self, other: 'Matrix'):
        return not self == other

    def __mul__(self, other: 'Matrix'):
        if (k := len(self.matrix[0])) != len(other.matrix):
            raise Exceptions.MatrixMultiplicationError(f'Rows quantity of the left matrix should be equal to Columns quantity of the right one')
        j, i = len(self.matrix), len(other.matrix[0])
        product = [[0 for _ in range(i)] for _ in range(j)]
        for j_ in range(j):
            for i_ in range(i):
                for k_ in range(k):
                    product[j_][i_] += self.matrix[j_][k_] * other.matrix[k_][i_]
        return Matrix(product)

    def __str__(self):
        return '\n'.join([' '.join([str(el) for el in row]) for row in self.matrix])

    def __repr__(self):
        return str(self)


m1 = Matrix(
    [
        [1, 2, 3],
        [4, 5, 6],
        [7, 8, 9]
    ]
)

m2 = Matrix(
    [
        [9, 8, 7],
        [6, 5, 4],
        [3, 2, 1]
    ]
)

m3 = Matrix(
    [
        [1, 2, 3, 4],
        [5, 6, 7, 8],
        [9, 10, 11, 12]
    ]
)

m4 = Matrix(
    [
        [1, 2, 3, 4, 5],
        [6, 7, 8, 9, 10],
        [11, 12, 13, 14, 15],
        [16, 17, 18, 19, 20]
    ]
)

print(f'matrix: \n{m1}')
print(f'sum: \n{m1 + m2}')
print(f'product1: \n{m1 * m2}')
print(f'product2: \n{m3 * m4}')

# Exceptions:

# ShapeMatrixError:
m_error = Matrix(
    [
        [1, 1],
        [1, 2, 3],
        [989]
    ]
)

# MatrixAdditionSubtractionError:
m_sum_error = m1 + m3

# MatrixMultiplicationError:
m_mult_error = m2 * m4
