# Dynamic programming -> accepted on codewars.com
def count(matrix: list[list[int]]) -> dict | int:
    squares_dictionary = {}
    # case of matrix with side.len = 0
    if len(matrix) == 0 or len(matrix[0]) == 0:
        return 0
    # side of the maximum square with its bottom right corner in (i,j)
    rows, cols = len(matrix), len(matrix[0])
    dyn_prog = [[0 for _ in range(cols)] for _ in range(rows)]  # dp memo
    # cycling all over the cells
    for i in range(rows):
        for j in range(cols):
            if matrix[i][j] == 1:
                # main recurrent relations
                if i == 0 or j == 0:
                    dyn_prog[i][j] = 1
                else:
                    dyn_prog[i][j] = min(dyn_prog[i - 1][j - 1], dyn_prog[i][j - 1], dyn_prog[i - 1][j]) + 1
                # building of squares dictionary
                current_square_len = dyn_prog[i][j]
                for k in range(2, current_square_len + 1):
                    if k in squares_dictionary.keys():
                        squares_dictionary[k] += 1
                    else:
                        squares_dictionary[k] = 1

    return squares_dictionary

chess_board = [
            [0, 1, 1, 1, 1],
            [1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1],
            [0, 1, 1, 0, 1],
            [1, 1, 1, 1, 1]
        ]
print(count(chess_board))