# accepted on codewars.com
calls_counter = 0

# Here we will be storing the information about placed numbers. According to the Sudoku-game rules,
#  We need to keep sets of rows, columns and squares so that the numbers do not repeat in these sets.
#  Thus, we should implement three 2D-arrays: rows, columns and squares

rows = []  # to keep the info about numbers used in the every row of the board given

columns = []  # to keep the info about numbers used in the every column of the board given

squares = []  # to keep the info about numbers used in the every square of the board given

#  board = []  # storing the board given

solution = []

board_size = 9  # size of the board
square_size = 3  # size of mini-squares

is_solved = False  # is Sudoku solved or not


# the main method that starts backtracking and placement of numbers into the board
def sudoku(board):
    """return the solved puzzle as a 2d array of 9 x 9"""
    global rows, columns, squares, solution, board_size, square_size, is_solved

    if not is_sudoku_valid(board):
        print('The board is not valid!')

    is_solved = False

    rows = [[0] * board_size for _ in range(board_size)]
    columns = [[0] * board_size for _ in range(board_size)]
    squares = [[0] * board_size for _ in range(board_size)]

    solution = [[0] * board_size for _ in range(board_size)]

    for j in range(board_size):
        for i in range(board_size):
            if board[j][i] != 0:
                place_number(board[j][i], j, i, board)  # adds every number on board to the sets

    recursive_seeker(0, 0, board)  # starts recursion

    if not is_solved:  # second one is enough
        print('There is no solution')

    # print_sudoku(solution)  # the solution if exists and is unique

    return solution


def copy_board_to_sol(solution_in, board_in):
    global board_size

    for i in range(board_size):
        for j in range(board_size):
            solution_in[j][i] = board_in[j][i]


def place_number(number: int, j: int, i: int, board_in):  # adds a number to the sets and on the board in the point of: board(j , i)
    global square_size

    index_square = square_size * (j // square_size) + i // square_size  # index of Sudoku-Square

    # calls_counter += 1

    rows[j][number - 1] = 1
    columns[i][number - 1] = 1
    squares[index_square][number - 1] = 1
    board_in[j][i] = number


def delete_number(number: int, j: int, i: int, board_in):  # deletes a number from the sets and from the board in the point of: board(j , i)
    global square_size

    index_square = square_size * (j // square_size) + i // square_size  # index of Sudoku-Square

    rows[j][number - 1] = 0
    columns[i][number - 1] = 0
    squares[index_square][number - 1] = 0
    board_in[j][i] = 0


def is_number_valid(number: int, j: int, i: int):  # checks could we place a number on board in the point of board(j , i), j refers to ROW whilst i refers to COLUMN
    global square_size, rows, columns, squares

    index_square = square_size * (j // square_size) + i // square_size

    return rows[j][number - 1] + columns[i][number - 1] + squares[index_square][number - 1] == 0


def recursive_seeker(j: int, i: int, board_in):  # backtracking
    global board_size, is_solved

    if board_in[j][i] == 0:  # if some number has already been placed in this cell
        for num in range(1, board_size + 1):
            if is_number_valid(num, j, i):  # if the placement is available
                place_number(num, j, i, board_in)  # placement of a number on board
                place_next(j, i, board_in)  # proceeding to the next number
                if not is_solved:
                    delete_number(num, j, i, board_in)  # a step of backtracking
                else:
                    return
    # if not, then we're making a new step
    else:
        place_next(j, i, board_in)


def place_next(j: int, i: int, board_in):  # a new step of backtracking
    global board_size, is_solved, solution

    if j == board_size - 1 and i == board_size - 1:  # if Sudoku is solved

        # PrintSudoku(board); // just some kind of testing


        copy_board_to_sol(solution, board_in)  # making a copy
        is_solved = True

    else:
        if i == board_size - 1:
            recursive_seeker(j + 1, 0, board_in)  # we are proceeding to the next row
        else:
            recursive_seeker(j, i + 1, board_in)  # just a new step to the right


def print_sudoku(board_in):  # just printing of a 2D array of chars
    global board_size

    for j in range(board_size):
        for i in range(board_size):
            print(board_in[j][i], end=' ')

        print()


def is_sudoku_valid(board_in):  # general check on validity
    global board_size

    if len(board_in) != 9 or len(board_in[0]) != 9:
        return False  # if the board has incorrect size

    for i in range(board_size):
        for j in range(board_size):
            if board_in[j][i] != 0:
                if board_in[j][i] < 1 or board_in[j][i] > 9:
                    return False

    return True  # IsSudokuValidRepeats(board); // next validation method call


new_board = [  # https://sudoku.com/ru/evil/ -> insane level of Sudoku 36ms
        [1, 0, 0, 4, 3, 0, 0, 5, 0],
        [0, 0, 5, 0, 0, 0, 9, 0, 0],
        [0, 0, 0, 0, 2, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 6, 0, 0, 0],
        [0, 8, 0, 0, 0, 0, 0, 0, 7],
        [3, 0, 0, 1, 5, 0, 0, 9, 0],
        [0, 3, 0, 6, 4, 0, 8, 0, 0],
        [0, 0, 0, 0, 0, 2, 0, 4, 0],
        [6, 0, 0, 0, 0, 9, 0, 0, 0]
    ]


sudoku(new_board)


# public static boolean IsSudokuValidRepeats(int[][] board) // checks if there is any repeating numbers in row/column or square 3*3
# {
#     int symbol;
#     int counter_of_points = 0;
#
#     HashSet<Integer> chars = new HashSet<Integer>(); // hash table for symbols
#
#     //Rows
#
#     for (int i = 0; i < 9; i++)
#     {
#         for (int j = 0; j < 9; j++)
#         {
#             symbol = board[i][j];
#             if (symbol != 0) chars.add(symbol);
#             else counter_of_points++;
#         }
#         if (chars.size() + counter_of_points != 9) return false;
#         chars.clear();
#         counter_of_points = 0;
#     }
#
#     //Columns
#
#     for (int i = 0; i < 9; i++)
#     {
#         for (int j = 0; j < 9; j++)
#         {
#             symbol = board[j][i];
#             if (symbol != 0) chars.add(symbol);
#             else counter_of_points++;
#         }
#         if (chars.size() + counter_of_points != 9) return false;
#         chars.clear();
#         counter_of_points = 0;
#     }
#
#     //Squares 3x3...
#
#     for (int i = 0; i < 9; i++)
#     {
#         for (int j = 0; j < 9; j++)
#         {
#             symbol = board[3 * (i / 3) + j / 3][3 * (i % 3) + j % 3];
#             if (symbol != 0) chars.add(symbol);
#             else counter_of_points++;
#         }
#         if (chars.size() + counter_of_points != 9) return false;
#         chars.clear();
#         counter_of_points = 0;
#     }
#
#     return true; // is Sudoku board valid?
# }
#
