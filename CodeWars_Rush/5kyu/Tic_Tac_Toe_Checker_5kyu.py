# accepted on codewars.com
def is_solved(board):
    # TODO: Check if the board is solved!

    if board[0][0] == 1 and board[1][1] == 1 and board[2][2] == 1:
        return 1
    elif board[0][0] == 2 and board[1][1] == 2 and board[2][2] == 2:
        return 2
    flag1 = False
    flag2 = False
    for i in range(3):
        flag1 = flag1 or set(board[i]) == {1}
        if flag1:
            return 1
        flag2 = flag2 or set(board[i]) == {2}
        if flag2:
            return 2
    flag1 = False
    flag2 = False
    for i in range(3):
        flag1 = flag1 or set([board[k][i] for k in range(3)]) == {1}
        if flag1:
            return 1
        flag2 = flag2 or set([board[k][i] for k in range(3)]) == {2}
        if flag2:
            return 2
    for j in range(3):
        for i in range(3):
            if board[j][i] == 0:
                return -1

    return 0


board = [[0, 0, 1],
         [0, 1, 2],
         [2, 1, 0]]

board1 = [[1, 1, 1],
         [0, 2, 2],
         [0, 0, 0]]

print(is_solved(board))

print(is_solved(board1))
