# accepted on codewars.com (1,2 and 4 kyu versions)
import time
from itertools import permutations as perms
# board section
board_size: int
board: list[list[int]]
# restrictions from simplify() if we proceeded to the backtracking section
board_restrictions: list[list[list[int]]]
# restrictions in order to avoid using the same numbers in one row or column
vertical_restrictions: dict
horizontal_restrictions: dict
# flag of finishing all the recursive branches
flag: bool

BOLD = "\033[1m"

BLACK = "\033[30m{}"
RED = "\033[31m{}"
GREEN = "\033[32m{}"
YELLOW = "\033[33m{}"
BROWN = "\033[34m{}"
PURPLE = "\033[35m{}"
CYAN = "\033[36m{}"

END = "\033[0m"

COLOURS = [RED, GREEN, YELLOW, BROWN, PURPLE, CYAN, BLACK]


# main method
def solve_puzzle(clues):
    global board_restrictions, board, board_size, horizontal_restrictions, vertical_restrictions, flag
    board_size = len(clues) // 4
    board = [[0] * board_size for _ in range(board_size)]

    # here we build valid permutations of skyscrapers' heights for the every row and column in the board given
    def generate_valid_permutations():
        all_possible_permutations = list(perms(range(1, board_size + 1)))  # all possible permutations of distinct heights without any validation
        valid_rows_perms, valid_columns_perms = [], []
        # here we are validating all the permutations above to in order to filter out the incorrect ones
        for index in range(board_size):
            # horizontal validation
            hor_pair = [clues[4 * board_size - 1 - index], clues[board_size + index]]
            valid_rows_perms.append([permutation for permutation in all_possible_permutations if
                                     (count_skyscrapers(permutation) == hor_pair[0] or not hor_pair[0]) and (
                                                 count_skyscrapers(permutation[::-1]) == hor_pair[1] or not hor_pair[1])])
            # vertical validation
            vert_pair = [clues[index], clues[3 * board_size - 1 - index]]
            valid_columns_perms.append([permutation for permutation in all_possible_permutations if
                                        (count_skyscrapers(permutation) == vert_pair[0] or not vert_pair[0]) and (
                                                count_skyscrapers(permutation[::-1]) == vert_pair[1] or not vert_pair[1])])

        return valid_rows_perms, valid_columns_perms

    print('generating the valid permutations: ')
    rows, columns = generate_valid_permutations()
    print('all the permutations been generated, here the lengths of them for the every row and column: ')
    print(f'in_rows: {[len(row) for row in rows]}, in_cols: {[len(col) for col in columns]}')  # check

    # now when we got the all valid permutations we can simplify the lists by filtering out some entries again
    def simplify():
        global board_restrictions
        if_simplified = False  # important flag -> it checks if the rows and columns valid permutations lists been changed or not to prevent the infinite loop case
        board_restrictions = [[[] for _ in range(board_size)] for _ in range(board_size)]
        # here we try to place all the possible numbers (from 1 to board size) at the every position (from (0, 0) to (6, 6))
        for j in range(board_size):
            for i in range(board_size):
                check_rows, check_columns = [], []
                for number in range(1, board_size + 1):
                    # we build two boolean arrays, every variable says if we can place the current number at this place (j, i) with the restrictions of rows[j] and columns[i] respectively
                    # rows
                    boolean_flag = False
                    for row in rows[j]:
                        if row[i] == number:
                            boolean_flag = True
                            break  # optimization
                    check_rows.append(boolean_flag)
                    # columns
                    boolean_flag = False
                    for col in columns[i]:
                        if col[j] == number:
                            boolean_flag = True
                            break  # optimization
                    check_columns.append(boolean_flag)

                # print(f'check rows: {check_rows}') -> further checking
                # print(f'check columns: {check_columns}')

                # if no number can be placed -> the puzzle cannot be solved!
                if check_rows.count(True) == 0 or check_columns.count(True) == 0:
                    print('the valid solution does not exist')
                    return False

                # if only one number can be placed -> we place this number
                if check_rows.count(True) == 1:
                    board[j][i] = (n := check_rows.index(True) + 1)
                    print(f'num: ({n}) been placed at ({j}, {i})')
                elif check_columns.count(True) == 1:
                    board[j][i] = (m := check_columns.index(True) + 1)
                    print(f'num: ({m}) been placed at ({j}, {i})')

                # here we filter out the valid permutations with weaker restrictions
                for k in range(board_size):
                    # if the restrictions are the same
                    if check_rows[k] == check_columns[k]:
                        if check_rows[k]:
                            board_restrictions[j][i].append(k + 1)
                        continue
                    # if rows restriction is weaker
                    if check_rows[k]:
                        rows[j] = [row for row in rows[j] if row[i] != k + 1]
                    # if columns restriction is weaker
                    elif check_columns[k]:
                        columns[i] = [col for col in columns[i] if col[j] != k + 1]
                    # if we reached this line -> we simplified our task -> we can proceed to the next level of simplification
                    if_simplified = True

        return if_simplified

    # simplification in cycle, while it has an impact
    print('simplifying begins...')
    simplify_steps_counter = 1
    print(f'{simplify_steps_counter}-th try of simplifying, rows: {[len(row) for row in rows]}, cols: {[len(col) for col in columns]}')  # check
    while simplify():
        simplify_steps_counter += 1
        print(f'{simplify_steps_counter}-th try of simplifying, rows: {[len(row) for row in rows]}, cols: {[len(col) for col in columns]}')  # check

    print('been simplified...')

    if ([len(row) for row in rows] + [len(col) for col in columns]).count(1) == 2 * board_size:
        print('the solution found: ')
        print(f'check: {check_board(board, rows, columns)}')
        return board

    # restrictions, needed in order to place only distinct numbers in rows and columns
    vertical_restrictions = {key: set() for key in range(board_size)}
    horizontal_restrictions = {key: set() for key in range(board_size)}

    # backtracking method -> it needs if simplify() could not get the solution
    def backtrack(j: int, i: int):
        global flag
        print(f'now entering: ({j},{i})')

        # border case of getting the right solution
        if j == board_size:
            print('SOME SOLUTION FOUND!!!')
            if check_board(board, rows, columns):
                print('check COMPLETED!')
                flag = False
            else:
                print('check been FAILED!!!')
            return

        # body of recursion
        for height in board_restrictions[j][i]:  # board_restrictions -> we got these restrictions from the last step of simplify method!
            if height not in horizontal_restrictions[j] and height not in vertical_restrictions[i]:
                if flag:
                    # doing
                    board[j][i] = height
                    horizontal_restrictions[j].add(height)
                    vertical_restrictions[i].add(height)
                    # recurrent relation
                    if i == board_size - 1:
                        backtrack(j + 1, 0)
                    else:
                        backtrack(j, i + 1)
                     # undoing
                    if flag:
                        board[j][i] = 0
                        horizontal_restrictions[j].remove(height)
                        vertical_restrictions[i].remove(height)

    flag = True
    print('backtracking starting: ')
    backtrack(0, 0)

    print('the solution found: ')
    return board


# counts skyscrapers from the left to the right (can be called for reversed array to count skyscrapers in the opposite direction)
def count_skyscrapers(array: list[int]):
    counter, max_height = 0, 0
    for el in array:
        if el > max_height:
            max_height = el
            counter += 1

    return counter


def check_board(board_to_check, rows, columns):
    for j in range(len(board_to_check)):
        if tuple(board_to_check[j]) not in rows[j]:
            return False
    for i in range(len(board_to_check)):
        if tuple([board_to_check[j][i] for j in range(len(board_to_check))]) not in columns[i]:
            return False
    return True


def colour_print(char, colour):
    print(f"{(BOLD + colour.format(char) + END)}", end=' ')


def show_line(length: int):
    print(f"*{'-' * (2 * length + 1)}*")


def show_puzzle(solved_puzzle: list[list[int]]):
    show_line(len(solved_puzzle[0]))
    for row in solved_puzzle:
        print(f'|', end=' ')
        for cell in row:
            colour_print(cell, COLOURS[cell - 1])
        print(f'|')
    show_line(len(solved_puzzle[0]))


t1 = time.perf_counter_ns()

# print(solve_puzzle([0, 2, 3, 0, 2, 0, 0, 5, 0, 4, 5, 0, 4, 0, 0, 4, 2, 0, 0, 0, 6, 0, 0, 0, 0, 0, 0, 0]))
# print(solve_puzzle([7, 0, 0, 0, 2, 2, 3, 0, 0, 3, 0, 0, 0, 0, 3, 0, 3, 0, 0, 5, 0, 0, 0, 0, 0, 5, 0, 4]))
show_puzzle(solve_puzzle([3, 3, 2, 1, 2, 2, 3, 4, 3, 2, 4, 1, 4, 2, 2, 4, 1, 4, 5, 3, 2, 3, 1, 4, 2, 5, 2, 3]))

t2 = time.perf_counter_ns()

print(f'time elapsed: {(t2 - t1) / 10 ** 6} milliseconds')
