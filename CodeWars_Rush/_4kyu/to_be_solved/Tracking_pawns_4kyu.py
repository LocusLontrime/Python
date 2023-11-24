# accepted on codewars.com
walk = ((0, 1), (1, 0), (0, -1), (-1, 0))
cols = {'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5, 'g': 6, 'h': 7}
SIZE = 8
symbols = ['p', 'P']  # 'P' means whites and 'p' means blacks...


def pawn_move_tracker(moves: list[str]):
    board = [
        [".", ".", ".", ".", ".", ".", ".", "."],
        ["p", "p", "p", "p", "p", "p", "p", "p"],
        [".", ".", ".", ".", ".", ".", ".", "."],
        [".", ".", ".", ".", ".", ".", ".", "."],
        [".", ".", ".", ".", ".", ".", ".", "."],
        [".", ".", ".", ".", ".", ".", ".", "."],
        ["P", "P", "P", "P", "P", "P", "P", "P"],
        [".", ".", ".", ".", ".", ".", ".", "."]
    ]
    # main cycle:
    for turn, move in enumerate(moves):  # turn % 2 = 0 for whites and 1 for blacks...
        print(f'turn, move: {turn, move}')
        white_moving = turn % 2 == 0
        print(f'white_moving: {white_moving}')
        # defines the type of move:
        if len(move) == 2:
            # 1. moving:
            print(f'moving...')
            j_, i_ = parse_move(move)
            # check for validity of moving (the place for moving is empty):
            if board[j_][i_] == '.':
                # first pawn's move case:
                if j_ == 4 - 1 and board[2 - 1][i_] == symbols[int(white_moving)]:
                    # moving itself (updating the board):
                    board[j_][i_] = symbols[int(white_moving)]
                    board[2 - 1][i_] = '.'
                    continue
                if j_ == 5 - 1 and board[7 - 1][i_] == symbols[int(white_moving)]:
                    # moving itself (updating the board):
                    board[j_][i_] = symbols[int(white_moving)]
                    board[7 - 1][i_] = '.'
                    continue
                # pawn's current position:
                _j, _i = (j_ + 1 if white_moving else j_ - 1), i_
                # the position should be valid
                if is_valid(_j, _i):
                    # a pawn should be found at this position:
                    if board[_j][_i] == symbols[int(white_moving)]:
                        # moving itself (updating the board):
                        board[j_][i_] = symbols[int(white_moving)]
                        board[_j][_i] = '.'
                    else:
                        return f'{move} is invalid'
            else:
                return f'{move} is invalid'
        else:
            # 2. capturing:
            print(f'capturing...')
            _i, j_, i_ = parse_capture(move)
            # check for validity of moving (the pawn is at the right place and has an opposite colour):
            if board[j_][i_] == symbols[(int(white_moving) + 1) % 2]:
                # current position of the capturing pawn:
                _j, _i = (j_ + 1 if white_moving else j_ - 1), _i
                # the position should be valid
                if is_valid(_j, _i):
                    # the capturing pawn should be found at this position:
                    if board[_j][_i] == symbols[int(white_moving)]:
                        # moving itself (updating the board):
                        board[j_][i_] = symbols[int(white_moving)]
                        board[_j][_i] = '.'
                    else:
                        return f'{move} is invalid'
            else:
                return f'{move} is invalid'
    return board


def parse_move(move: str) -> tuple[int, int]:
    return SIZE - int(move[1]), cols[move[0]]


def parse_capture(move: str) -> tuple[int, int, int]:
    return cols[move[0]], *parse_move(move[2:])


def is_valid(j: int, i: int) -> bool:
    return 0 <= j < SIZE and 0 <= i < SIZE


def print_board(board) -> None:
    for row in board:
        print(f'{row}')


# print(f'move: {parse_move(f"c2")}')
# print(f'capture: {parse_capture(f"dxc5")}')

ex = ["d4", "d5", "f3", "c6", "f4", "c5", "dxc5"]  # ["e6"]  # ["e4", "d5", "exf5"]  # ["d4", "d5", "f3", "c6", "f4"]
res = pawn_move_tracker(ex)
print_board(res)
