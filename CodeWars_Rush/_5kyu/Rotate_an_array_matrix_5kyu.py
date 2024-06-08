# accepted on codewars.com


def rotate(matrix, direction) -> list[list[int]]:
    n, m = len(matrix), len(matrix[0])
    matrix_ = [[0 for _ in range(n)] for _ in range(m)]
    for j in range(n):
        for i in range(m):
            j_, i_ = (i, n - 1 - j) if direction == 'clockwise' else (m - 1 - i, j)
            print(f'{j, i} -> {j_, i_}')
            matrix_[j_][i_] = matrix[j][i]
    return matrix_


_matrix = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9]
]

__matrix = [[1, 2, 3]]


new_matrix = rotate(__matrix, 'anti-clockwise')

print(f'rotated matrix: ')
for row in new_matrix:
    print(f'{row}')








