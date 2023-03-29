import random

MAX_SUCCESSFUL_PLACEMENTS = 4


def solve_chess_puzzle(queens: list[str]):
    ys, xs, d1, d2 = [set() for _ in range(4)]
    queens_counter = 0
    for y, row in enumerate(queens):
        for x, ch in enumerate(row):
            if ch == 'Q':
                queens_counter += 1
                # adding queen's coords in to the sets:
                ys.add(y)
                xs.add(x)
                d1.add(y + x)
                d2.add(y - x)
                if not (len(ys) == len(xs) == len(d1) == len(d2) == queens_counter):
                    return False
    return True


def random_check(chess_size: int = 8):
    counter_of_successful_placements = 0
    counter = 0
    while counter_of_successful_placements < MAX_SUCCESSFUL_PLACEMENTS:
        chess_board = [['_' for _ in range(chess_size)] for _ in range(chess_size)]
        counter += 1
        i_set = [_ for _ in range(chess_size)]
        for j in range(chess_size):
            random.shuffle(i_set)
            i = i_set.pop()
            chess_board[j][i] = 'Q'
        chess_board_ = [''.join(row) for row in chess_board]
        if solve_chess_puzzle(chess_board_):
            print(f'successful placement {counter_of_successful_placements + 1}: \n')
            for row in chess_board_:
                print(f'{row}')
            print()
            counter_of_successful_placements += 1
    print(f'all {MAX_SUCCESSFUL_PLACEMENTS} successful placements has been found within {counter} iterations')


queens_ = [
    'Q   ',
    '   Q',
    ' Q Q',
    '  Q '
]

queens_true = [
    ' Q  ',
    '   Q',
    'Q   ',
    '  Q '
]

if __name__ == '__main__':
    print(f'res: {solve_chess_puzzle(queens_true)}\n')
    random_check()



