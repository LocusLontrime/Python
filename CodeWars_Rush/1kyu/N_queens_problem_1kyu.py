# accepted on codewars.com
import random
import math
import time

conflicts_threshold = 3


# main method
def solve_n_queens(size, mandatory_coords):

    # here we use the simple bactracking
    if size <= 10:
        answer = queens_backtrack(size, mandatory_coords)
        return get_string_of_queens(size, answer) if answer is not None else None

    attempts_made = 1

    while True:

        partial_sol = generate_greed(size, mandatory_coords)
        solution = conflicts_solver(partial_sol, size, mandatory_coords)

        if not solution and (attempts_made <= 15):
            # print(str(size) + ": no solution been found", sep='')
            attempts_made += 1
        else:
            if attempts_made <= 15:
                # print(str(size) + ": SOLUTION BEEN FOUND!!!", sep='')
                # print("Time elapsed: ", time.time() - start, "seconds.")
                return get_string_of_queens(size, solution)
            else:
                # print(str(size) + ": Tries ended up", sep='')
                # print("Time elapsed", time.time() - start, "seconds.")
                return None


# here we are building a partial solution for the task given
def generate_greed(n, mandatory: list[int]):
    # initializating
    positions = [-1] * n
    verticals = [-1] * n
    diagonals = [[0 for x in range((2 * n) - 1)] for y in range(2)]

    # mandatory queen
    positions[mandatory[0]] = mandatory[1]
    verticals[mandatory[1]] = 1
    diagonals[0][mandatory[0] + mandatory[1]] = 1
    diagonals[1][n - 1 + mandatory[0] - mandatory[1]] = 1

    marked_rows = []
    cols = set()

    for c in range(n):
        if c == mandatory[1]:
            continue
        cols.add(c)

    for row in range(n):
        if row == mandatory[0]:
            continue

        for col in cols:

            if (diagonals[0][row + col] == 0) and (diagonals[1][row + ((n - 1) - col)] == 0):
                positions[row] = col
                verticals[col] = 1
                diagonals[0][row + col] = 1
                diagonals[1][row + ((n - 1) - col)] = 1
                cols.remove(col)
                break

        if positions[row] == -1:
            marked_rows.append(row)

    for row in marked_rows:
        col = cols.pop()
        positions[row] = col
        verticals[col] = 1
        diagonals[0][row + col] += 1
        diagonals[1][row + ((n - 1) - col)] += 1

    return [positions, verticals, diagonals]


# now fixing the prev solution, the way is: min conflicts algorithm
def conflicts_solver(queens, size, mandatory):
    diagonals = queens.pop()
    verticals = queens.pop()
    positions = queens.pop()
    length = len(positions)

    problem_cols = get_conflicts([positions, verticals, diagonals], mandatory)

    swaps_counter = 0
    err_flag = False

    def place(r, c):
        verticals[c] -= 1
        diagonals[0][r + c] -= 1
        diagonals[1][r + ((length - 1) - c)] -= 1

    def displace(r, new_c):
        verticals[new_c] += 1
        diagonals[0][r + new_c] += 1
        diagonals[1][r + ((length - 1) - new_c)] += 1

    while problem_cols:

        random.shuffle(problem_cols)
        row = problem_cols.pop()
        conflicts = []
        min_conflicts = []
        the_min = math.inf

        for col in range(length):

            if col == mandatory[1]:
                conflicts.append(0)
                continue

            conflicts.append(0)
            conflicts[col] += verticals[col]
            conflicts[col] += diagonals[0][row + col]
            conflicts[col] += diagonals[1][row + ((length - 1) - col)]

            if col == positions[row]:
                conflicts[col] = math.inf

            if conflicts[col] < the_min:
                min_conflicts = []
                the_min = conflicts[col]

            if conflicts[col] == the_min:
                min_conflicts.append(col)

        # now let's swap
        random.shuffle(min_conflicts)
        swap = min_conflicts.pop()
        col = positions[row]

        place(row, col)

        displace(row, swap)

        positions[row] = swap

        # restriction for no solution or bad variation
        if swaps_counter < size * conflicts_threshold:
            problem_cols = get_conflicts([positions, verticals, diagonals], mandatory)
        else:
            err_flag = True
            break

        swaps_counter += 1

    return [] if err_flag else positions


# getting all the queens in conflicts:
def get_conflicts(array, mandatory):
    diagonals = array.pop()
    verticals = array.pop()
    positions = array.pop()

    length = len(positions)
    conflicts = []

    for col in range(length):

        if col != mandatory[1]:

            row = positions[col]

            if verticals[row] > 1 or diagonals[0][row + col] > 1 or diagonals[1][col + ((length - 1) - row)] > 1:
                conflicts.append(col)  # col

    return conflicts


# translating the coords to string
def get_string_of_queens(size, sol):
    res = ''

    for coords in sol:
        res += '.' * coords + 'Q' + '.' * (size - 1 - coords) + '\n'

    return res


flag_of_rec_stop: bool  # 36 366 98 989
result: list


# bactracking auxiliary method
def queens_backtrack(n: int, mandatory):
    global flag_of_rec_stop, result

    result = []
    flag_of_rec_stop = False

    def recursive_seeker(row: int, vertical_set: list[int],
                         diag1_set: set[int], diag2_set: set[int],
                         board_size: int) -> None:
        global flag_of_rec_stop, result

        # jumping over the mandatory queen
        if row == mandatory[0]:
            recursive_seeker(row + 1, vertical_set + [mandatory[1]], diag1_set, diag2_set, board_size)

        # finishing all the branches of recursion tree
        if flag_of_rec_stop:
            return

        # catching the result
        if row == board_size:
            for i in range(board_size):
                if i == mandatory[0]:
                    result.append(mandatory[1])
                else:
                    result.append(vertical_set[i])

            flag_of_rec_stop = True
            return

        # cycling all over the possible vertical coords:
        for i in range(board_size):
            if i not in (vertical_set + [mandatory[1]]) and row + i not in diag1_set and row - i not in diag2_set:
                new_vertical_set = list(vertical_set)
                new_diag1_set = set(diag1_set)
                new_diag2_set = set(diag2_set)

                new_vertical_set.append(i)
                new_diag1_set.add(row + i)
                new_diag2_set.add(row - i)

                recursive_seeker(row + 1, new_vertical_set, new_diag1_set, new_diag2_set, board_size)
                # no need to bactrack coz of creating new sets

    recursive_seeker(0, [], {mandatory[0] + mandatory[1]}, {mandatory[0] - mandatory[1]}, n)

    return result if len(result) > 0 else None


start = time.time_ns()

print(solve_n_queens(100, [1, 2]))

finish = time.time_ns()

print(f'Time costs: {(finish - start) // 10 ** 6} milliseconds')


