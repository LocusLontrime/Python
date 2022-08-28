import time
from functools import reduce

board_size: int
rec_counter = 0
board_restrictions: list[list[int]]
board: list[list[int]]
vertical_restrictions: dict
horizontal_restrictions: dict
flag: bool


def solve_puzzle(clues):
    global board_size, board_restrictions, board, vertical_restrictions, horizontal_restrictions, flag
    board_size = len(clues) // 4
    print(f'board_size: {board_size}')
    board_restrictions = [[board_size] * board_size for _ in range(board_size)]
    board = [[0] * board_size for _ in range(board_size)]

    for i in range(board_size):
        curr_restriction = find_restrictions(clues[i], clues[3 * board_size - 1 - i])
        for j in range(board_size):
            if curr_restriction[j] < board_restrictions[j][i]:
                board_restrictions[j][i] = curr_restriction[j]

    for j in range(board_size):
        curr_restriction = find_restrictions(clues[4 * board_size - 1 - j], clues[board_size + j])
        for i in range(board_size):
            if curr_restriction[i] < board_restrictions[j][i]:
                board_restrictions[j][i] = curr_restriction[i]

    print(board_restrictions)
    vertical_restrictions = {key: set() for key in range(board_size)}
    horizontal_restrictions = {key: set() for key in range(board_size)}

    # backtracking:
    def backtracking(curr_j: int, curr_i: int):
        # if curr_j > 4: print(f'now entering ({curr_j, curr_i})')
        global board, vertical_restrictions, horizontal_restrictions, flag
        if curr_j == board_size:
            flag = False
            return

        def do():
            # do it:
            vertical_restrictions[curr_i].add(height)
            horizontal_restrictions[curr_j].add(height)

        def undo():
            # undo it
            if flag:
                vertical_restrictions[curr_i].remove(height)
                horizontal_restrictions[curr_j].remove(height)

        # body of rec:
        for height in range(1, board_restrictions[curr_j][curr_i] + 1):
            if height not in vertical_restrictions[curr_i] and height not in horizontal_restrictions[curr_j]:
                board[curr_j][curr_i] = height  # do
                hor_arr, vert_arr = board[curr_j][:curr_i + 1], [board[k][curr_i] for k in range(curr_j + 1)]
                if is_valid_new(hor_arr, clues[4 * board_size - 1 - curr_j], clues[board_size + curr_j]) and is_valid_new(vert_arr, clues[curr_i], clues[3 * board_size - 1 - curr_i]):
                    if flag:
                        do()
                        # recurrent relation:
                        if curr_i == board_size - 1:
                            backtracking(curr_j + 1, 0)
                        else:
                            backtracking(curr_j, curr_i + 1)

                        undo()
                if flag:
                    board[curr_j][curr_i] = 0  # undo

    flag = True
    backtracking(0, 0)

    res_tuple = tuple()

    for i in range(board_size):
        res_tuple += (tuple(board[i]),)

    return res_tuple


# def is_valid(arr: list[int], clue: int, is_left_clue=True, strict=False):
#     if clue == 0:
#         return True
#     counter, max_height = 0, 0
#     for el in arr if is_left_clue else list(reversed(arr)):
#         if el > max_height:
#             max_height = el
#             counter += 1
#
#     return counter <= clue if not strict else counter == clue


def is_valid_new(arr: list[int], left_clue: int, right_clue: int):
    # print(f'board size: {board_size}')
    right_tail = board_size - len(arr)

    def count(array: list[int], threshold: int):
        counter, max_height = 0, threshold
        for el in array:
            if el > max_height:
                max_height = el
                counter += 1

        return [counter, max_height]

    tail_array = set(range(1, board_size + 1)) - set(arr)
    max_height_tail = max(tail_array) if right_tail != 0 else 0
    l_counter, r_counter = count(arr, 0), count(list(reversed(arr)), max_height_tail)[0]

    # print(f'l counter: {l_counter}, r counter: {r_counter}, r tail: {right_tail}')

    if len(arr) == board_size:
        res = (l_counter[0] == left_clue or left_clue == 0) and (r_counter == right_clue or right_clue == 0)
    else:
        res = (l_counter[0] + (1 if max_height_tail > l_counter[1] else 0) <= left_clue <= l_counter[0] +
               reduce(lambda y, x: y + (1 if x > l_counter[1] else 0), tail_array, 0) or left_clue == 0) and (
                    r_counter + 1 <= right_clue <= r_counter + right_tail or right_clue == 0)

    # print(f'array: ({left_clue}){arr}({right_clue}) is {res}')

    return res


def find_restrictions(l_clue: int, r_clue: int) -> list[int]:
    global board_size
    res = [(board_size + 1 - l_clue + i) for i in range(l_clue - 1)] + [board_size] * (
            board_size + 2 - l_clue - r_clue) + [(board_size - i - 1) for i in range(r_clue - 1)]
    if l_clue == 0:
        res = res[1:]
    if r_clue == 0:
        res = res[:-1]

    return res


# board_size = 7
# print(find_right_perms(3, 2))  # [1, 2, 3, 4]

# x = find_restrictions(5, 3)
# print(f'length: {len(x)}, x: {x}')
# print(f'rec counter: {rec_counter}')
# print(solve_puzzle([2, 2, 1, 3, 2, 2, 3, 1, 1, 2, 2, 3, 3, 2, 1, 3]))
# print(solve_puzzle([3, 2, 2, 3, 2, 1,  1, 2, 3, 3, 2, 2,  5, 1, 2, 2, 4, 3,  3, 2, 1, 2, 2, 4]))
# print(solve_puzzle([0, 0, 0, 2, 2, 0, 0, 0, 0, 6, 3, 0, 0, 4, 0, 0, 0, 0, 4, 4, 0, 3, 0, 0]))


# print(solve_puzzle([7,0,0,0,2,2,3, 0,0,3,0,0,0,0, 3,0,3,0,0,5,0, 0,0,0,0,5,0,4]))
# print(solve_puzzle([0,0,5,0,0,0,6, 4,0,0,2,0,2,0, 0,5,2,0,0,0,5, 0,3,0,5,0,0,3]))
# print(find_restrictions(7, 0))
# print(find_restrictions(0, 7))
# print(find_restrictions(0, 0))
# print([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11][:-1])
# print([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11][1:])


def find_right_perms(l_clue: int, r_clue: int) -> list[list[int]]:
    global board_size, rec_counter

    rec_counter = 0

    permutations = []
    restrictions = [(board_size + 1 - l_clue + i) for i in range(l_clue - 1)] + [board_size] * (
            board_size + 2 - l_clue - r_clue) + [(board_size - i - 1) for i in range(r_clue - 1)]

    print(f'restrictions: {restrictions}')

    def recursive_seeker(curr_permutation: list[int], rec_depth: int, max_left_height: int, left_counter: int) -> None:
        global rec_counter

        rec_counter += 1

        # border case:
        if rec_depth == board_size:
            if left_counter == l_clue or l_clue == 0:
                right_counter, max_right_height = 0, 0
                for i in range(board_size - 1, -1, -1):
                    if curr_permutation[i] > max_right_height:
                        max_right_height = curr_permutation[i]
                        right_counter += 1
                if right_counter == r_clue or r_clue == 0:
                    permutations.append(curr_permutation)
            return

        # body of rec:
        for i in range(1, restrictions[rec_depth] + 1):
            # recurrent relation:
            if i not in curr_permutation:
                if left_counter <= l_clue or l_clue == 0:
                    recursive_seeker(curr_permutation + [i], rec_depth + 1,
                                     *(i, left_counter + 1) if i > max_left_height else (max_left_height, left_counter))

    # rec call
    recursive_seeker([], 0, 0, 0)

    return permutations


# perms_of_7 = find_right_perms(6, 2)
# print(f'length: {len(perms_of_7)}, list: {perms_of_7}')
# print(f'rec counter: {rec_counter}')
#
# print(is_valid([1, 2, 3, 4, 5, 7, 6], 6, True))
# print(is_valid([1, 2, 3, 4, 5, 7, 6], 2, False))
#
# print([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11][:5])

# print(is_valid_new([1, 5, 3, 4], 2, 5))
# print(is_valid_new([2, 3, 6, 7], 4, 3))
# print(is_valid_new([1, 2, 3, 4, 5, 6, 7], 7, 1))

# board_size = 6
# print(is_valid_new([5, 2, 6, 1, 3], 2, 2))
# print(is_valid_new([1, 2, 3, 4, 5, 6], 6, 1))
# print(is_valid_new([6, 5, 4, 3, 2, 1], 1, 6))
# print(is_valid_new([1, 2, 3, 4, 5, 6], 6, 2))
# print(is_valid_new([3, 2, 1, 4, 6], 3, 2))

# print(solve_puzzle([0, 0, 0, 2, 2, 0, 0, 0, 0, 6, 3, 0, 0, 4, 0, 0, 0, 0, 4, 4, 0, 3, 0, 0]))
# print(solve_puzzle([0, 3, 0, 5, 3, 4, 0, 0, 0, 0, 0, 1, 0, 3, 0, 3, 2, 3, 3, 2, 0, 3, 1, 0]))
# print(solve_puzzle([7, 0, 0, 0, 2, 2, 3, 0, 0, 3, 0, 0, 0, 0, 3, 0, 3, 0, 0, 5, 0, 0, 0, 0, 0, 5, 0, 4]))
# print(solve_puzzle([0, 0, 5, 0, 0, 0, 6, 4, 0, 0, 2, 0, 2, 0, 0, 5, 2, 0, 0, 0, 5, 0, 3, 0, 5, 0, 0, 3]))
# print(solve_puzzle([0, 2, 3, 0, 2, 0, 0, 5, 0, 4, 5, 0, 4, 0, 0, 4, 2, 0, 0, 0, 6, 5, 2, 2, 2, 2, 4, 1]))
# print(solve_puzzle([3, 3, 2, 1, 2, 2, 3, 4, 3, 2, 4, 1, 4, 2, 2, 4, 1, 4, 5, 3, 2, 3, 1, 4, 2, 5, 2, 3]))
# print(solve_puzzle([0, 2, 3, 0, 2, 0, 0, 5, 0, 4, 5, 0, 4, 0, 0, 4, 2, 0, 0, 0, 6, 0, 0, 0, 0, 0, 0, 0]))

t1 = time.perf_counter_ns()

print(solve_puzzle([0, 0, 0, 2, 2, 0, 0, 0, 0, 6, 3, 0, 0, 4, 0, 0, 0, 0, 4, 4, 0, 3, 0, 0]))

t2 = time.perf_counter_ns()

print(f'time elapsed: {(t2 - t1) / 10 ** 9} seconds')
