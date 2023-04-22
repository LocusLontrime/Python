class MatrixError(Exception):
    ...


class ShapeMatrixError(MatrixError):
    def __init__(self, s):
        super().__init__(s)


class MatrixAdditionSubtractionError(MatrixError):
    def __init__(self, s):
        super().__init__(s)


class MatrixMultiplicationError(MatrixError):
    def __init__(self, s):
        super().__init__(s)


if __name__ == '__main__':
    print(f'{ShapeMatrixError("lalala")}')
