CONST = 2 << 32


def set_zeroes(matrix) -> None:
    # linear sizes:
    max_j, max_i = len(matrix), len(matrix[0])
    # the core algo (we will use cells like matrix[0][i] and matrix [j][0] as an aux array
    # so that remove all rows and cols with 0 in the beginning:
    if matrix[0][0]:
        matrix[0][0] = [matrix[0][0], matrix[0][0]]
    else:
        matrix[0][0] = [CONST, CONST]
    print(f'{matrix[0][0] = }')
    for j in range(max_j):
        for i in range(max_i):
            if matrix[j][i] == 0:
                if j:
                    matrix[j][0] = CONST
                else:
                    matrix[0][0][0] = CONST
                if i:
                    matrix[0][i] = CONST
                else:
                    matrix[0][0][1] = CONST
    print(f'{matrix[0][0] = }')
    # rows clear:
    for j in range(1, max_j):
        if matrix[j][0] == CONST:
            clear_row(j, max_i, matrix)
    # columns clear:
    for i in range(1, max_i):
        if matrix[0][i] == CONST:
            clear_column(i, max_j, matrix)
    # (0,0) point processing:
    if matrix[0][0][0] == CONST and matrix[0][0][1] == CONST:
        clear_row(0, max_i, matrix)
        clear_column(0, max_j, matrix)
    elif matrix[0][0][1] == CONST:
        clear_column(0, max_j, matrix)
    elif matrix[0][0][0] == CONST:
        clear_row(0, max_i, matrix)
    else:
        matrix[0][0] = matrix[0][0][0]
    for row in matrix:
        print(f'{row}')


def clear_row(j: int, max_i: int, matrix: list[list[int]]) -> None:
    for i in range(max_i):
        matrix[j][i] = 0


def clear_column(i: int, max_j: int, matrix: list[list[int]]) -> None:
    for j in range(max_j):
        matrix[j][i] = 0


def xuita(array: list[int]):
    for el in array:
        el = 98
    print(f'{array = }')


test_ex = [
    [0, 1, 2, 0],
    [3, 4, 5, 2],
    [1, 3, 1, 5]
]

test_ex_1 = [
    [1, 1, 1],
    [1, 0, 1],
    [1, 1, 1]
]

print(f'test ex res -> {set_zeroes(test_ex)}')                                        # 36 366 98 989 98989 LL LL
print(f'test ex 1 res -> {set_zeroes(test_ex_1)}')

print(f'{xuita([9, 98, 98989])}')
