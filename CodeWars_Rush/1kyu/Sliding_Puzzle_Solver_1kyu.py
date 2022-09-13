# accepted on codewars.com
import time

rec_flag: bool
rec_seeker_counter: int


def slide_puzzle(ar):
    board = SlidingBoard(ar)
    return board.solve_puzzle()


class SlidingBoard:
    def __init__(self, puzzle: list[list[int]]) -> None:
        self.max_j, self.max_i = len(puzzle), len(puzzle[0])
        # initial board state, will be modified during the solution phase:
        self.sliding_board = [[Cell(puzzle[j][i], j, i) for i in range(self.max_i)] for j in range(self.max_j)]
        self.solved_board = [[1 + j * self.max_i + i for i in range(self.max_i)] for j in
                             range(self.max_j)]  # filling in the final values
        self.solved_board[-1][-1] = 0  # ending zero
        self.solution = []  # the final sequence of actions
        # now we are getting all the possible directions from the every cell on the sliding puzzle:
        for row in self.sliding_board:
            for cell in row:
                # all possible ways from the cell
                cell.get_ways(self.sliding_board, self.max_j, self.max_i)

    def solve_puzzle(self):
        # solving the rows except two last ones
        for j in range(self.max_j - 2):
            # print(f'SOLVING ROW: {j}')
            self.solve_row(j)
        # the last two rows we solve per column until the 2x2 board remains
        for i in range(self.max_i - 2):
            # locating the "rightmost" two cells if we look at rotated two rows
            upper, lower = self.sliding_board[-1][i], self.sliding_board[-1][i + 1]
            upper_right_num, lower_right_num = self.solved_board[-2][i], self.solved_board[-1][i]
            if (c1 := self.sliding_board[-2][i]).num == upper_right_num and (
                    c2 := self.sliding_board[-1][i]).num == lower_right_num:
                c1.is_located_right, c2.is_located_right = True, True
            else:
                # here we locate the lower cell in the column at the special position
                self.locate_cell(upper_right_num, upper, False)
                self.locate_cell(lower_right_num, self.sliding_board[-2][i + 2], False)
                self.locate_cell(upper_right_num, upper, False)
                self.locate_cell(lower_right_num, lower, False)
                # then locate and frieze
                self.locate_cell(upper_right_num)
                self.locate_cell(lower_right_num)

        if self.solve_2_x_2_square() is False:
            return None

        return self.solution

    def solve_row(self, j: int):
        # locating all cells except the rightmost two
        for i in range(self.max_i - 2):
            right_num = self.solved_board[j][i]
            # print(f'SOLVING NUM: {right_num}')
            self.locate_cell(right_num)

        # locating the rightmost two cells
        last, prev = self.sliding_board[j][-2], self.sliding_board[j + 1][-2]
        prev_right_num, last_right_num = self.solved_board[j][-2], self.solved_board[j][-1]
        if (c1 := self.sliding_board[j][-2]).num == prev_right_num and (
                c2 := self.sliding_board[j][-1]).num == last_right_num:
            c1.is_located_right, c2.is_located_right = True, True
        else:
            # common sequence, at first we prepare
            self.locate_cell(last_right_num, last, False)
            self.locate_cell(prev_right_num, self.sliding_board[j + 2][-1], False)
            self.locate_cell(last_right_num, last, False)
            self.locate_cell(prev_right_num, prev, False)
            # then locate and frieze
            self.locate_cell(last_right_num)
            self.locate_cell(prev_right_num)

    def solve_2_x_2_square(self):
        # checks if the puzzle solvable:
        a, b, c = (m := (self.max_j - 1) * self.max_i) - 1, m, m + self.max_i - 1
        # print(f'a, b, c: {a, b, c}')
        if not self.locate_cell(a) or not self.locate_cell(b) or not self.locate_cell(c):
            return False

        return True

    def locate_cell(self, num: int, goal_cell=None, frieze_or_not=True):
        # checking for this has been already solved:

        # the whole path itself from the zero to the right position of the num
        whole_path = []
        # the right position coordinates
        rj, ri = (num - 1) // self.max_i, (num - 1) % self.max_i
        # print(f'right j: {rj}, right i: {ri}')
        goal = self.sliding_board[rj][ri] if goal_cell is None else goal_cell
        # print(f'GOAL INITIAL J: {goal.j}, I: {goal.i}')
        # pathfinding cycle
        while 1 == 1:  # just a fun
            if goal.num == num:
                if frieze_or_not:
                    goal.is_located_right = True
                break

            # print(f'GOAL NUM: {goal.num}, goal j: {goal.j}, goal i: {goal.i}')

            zero_cell = self.find_number_cell(0)
            num_cell = self.find_number_cell(num)
            nearest = num_cell.get_nearest_to(goal)
            # print(f'zero coords: ({zero_cell.j, zero_cell.i})')
            # print(f'num_cell coords: ({num_cell.j, num_cell.i})')
            # print(f'nearest coords: ({nearest.j, nearest.i})')

            a_path = zero_cell.find_the_path_of_zero_to_aim(nearest, num_cell)

            if a_path is None:
                return False

            whole_path += (pa := [a_path[index].num for index in range(1, len(a_path))])

            for ind in range(len(a_path) - 1):
                a_path[ind].move(a_path[ind + 1])

            whole_path.append(num)
            num_cell.move(nearest)

            # print(f'a_path: {pa + [num]}')

            # self.show_puzzle()

        self.solution += whole_path
        return True

    def find_number_cell(self, num: int) -> 'Cell':
        for j in range(self.max_j):
            for i in range(self.max_i):
                if (c := self.sliding_board[j][i]).num == num:
                    return c

    def show_puzzle(self):
        for row in self.sliding_board:
            print(row)


class Cell:  # unmovable
    directions = [[-1, 0], [0, 1], [1, 0], [0, -1]]  # static var for 4 possible directions

    # checks if the moving in that direction is valid
    @staticmethod
    def is_direction_valid(j: int, i: int, max_j: int, max_i: int):
        return 0 <= j < max_j and 0 <= i < max_i

    def __init__(self, num: int, j: int, i: int) -> None:
        self.num = num  # number currently located in the cell, starts with initial value
        self.possible_ways: list['Cell'] = list()  # possible directions of further moving, max length is 4
        self.is_located_right = False  # flag of right locating
        self.j, self.i = j, i  # coordinates

    def __repr__(self):
        return str(self.num)

    def move(self, other: 'Cell'):
        self.num, other.num = other.num, self.num
        # self.is_located_right, other.is_located_right = other.is_located_right, self.is_located_right

    def calc_manhattan_distance(self, other: 'Cell') -> int:
        return abs(self.j - other.j) + abs(self.i - other.i)

    def get_ways(self, sliding_board: list[list['Cell']], max_j: int, max_i: int) -> None:
        for direction in Cell.directions:
            if Cell.is_direction_valid((new_j := self.j + direction[0]), (new_i := self.i + direction[1]), max_j,
                                       max_i):
                self.possible_ways.append(sliding_board[new_j][new_i])

    def get_nearest_to(self, aim: 'Cell') -> 'Cell':
        # method for sorting
        def sort_key(x):
            return x[1]

        # elements for selection
        elements: list[tuple['Cell', int]] = []
        for way in self.possible_ways:
            if not way.is_located_right:
                elements.append((way, way.calc_manhattan_distance(aim)))
        # sorting
        elements = sorted(elements, key=sort_key)
        # print(f'elements: {elements}')
        # returning the nearest to the aim adjacent to self cell
        return elements[0][0]

    # a star variation, not the shortest way, but min calls of rec
    def find_the_path_of_zero_to_aim(self, aim: 'Cell', pivot_num: 'Cell'):
        global rec_flag, rec_seeker_counter
        rec_flag = True
        rec_seeker_counter += 0

        def rec_seeker(curr_cell: 'Cell', curr_path: list['Cell'], visited_cells: set['Cell']):
            global rec_flag, rec_seeker_counter
            rec_seeker_counter += 1
            # border case:
            if curr_cell == aim:
                rec_flag = False
                return curr_path
            # body of recursion:
            ways_to_be_sorted = list()  # list[tuple['Cell', int]]
            for next_call in curr_cell.possible_ways:
                if next_call not in visited_cells and next_call != pivot_num and not next_call.is_located_right:
                    ways_to_be_sorted.append((next_call, next_call.calc_manhattan_distance(aim)))
            # prioritizing the way:
            ans = None
            for best_way in sorted(ways_to_be_sorted, key=lambda x: x[1]):
                if rec_flag:
                    visited_cells.add(best_way[0])
                    ans = ans or rec_seeker(best_way[0], curr_path + [best_way[0]], visited_cells)
                    visited_cells.remove(best_way[0])

            return ans

        path = rec_seeker(self, [self], {self})

        return path


puzzle = [
    [1, 3, 5, 6],
    [14, 13, 10, 11],
    [2, 4, 9, 8],
    [12, 7, 15, 0]
]

p = [
    [1, 26, 15, 13, 25, 16, 19, 28, 8, 20],
    [23, 3, 65, 4, 34, 33, 46, 39, 9, 30],
    [11, 2, 27, 47, 7, 35, 14, 6, 17, 29],
    [42, 24, 0, 41, 31, 58, 90, 10, 40, 50],
    [52, 12, 43, 21, 37, 69, 53, 38, 48, 67],
    [62, 74, 51, 61, 54, 36, 70, 55, 45, 59],
    [5, 22, 80, 68, 63, 18, 88, 32, 79, 99],
    [92, 56, 49, 91, 76, 87, 44, 75, 78, 98],
    [94, 71, 72, 73, 95, 64, 60, 97, 96, 85],
    [81, 83, 66, 93, 84, 77, 82, 86, 57, 89]
]

puzzle_10 = [
    [23, 1, 0, 3, 25, 18, 38, 10, 29, 58],
    [12, 4, 11, 24, 5, 15, 7, 40, 19, 30],
    [32, 2, 35, 34, 45, 16, 8, 9, 20, 39],
    [61, 13, 42, 6, 14, 26, 36, 46, 50, 66],
    [31, 62, 74, 21, 17, 47, 22, 49, 77, 76],
    [73, 43, 44, 94, 69, 67, 28, 59, 90, 97],
    [72, 51, 83, 55, 82, 85, 80, 57, 89, 95],
    [33, 65, 52, 56, 63, 87, 88, 98, 79, 27],
    [92, 91, 71, 60, 41, 81, 86, 96, 70, 99],
    [75, 93, 54, 68, 84, 53, 64, 37, 78, 48]
]

puzzle_x = [
    [4, 1, 3],
    [2, 8, 0],
    [7, 6, 5]
]

puzzle_non_sol = [
    [2, 0, 7],
    [1, 4, 5],
    [8, 6, 3]
]

puzzle_app = [
    [1, 16, 27, 4, 14, 17, 38],
    [44, 45, 6, 29, 30, 48, 33],
    [2, 19, 37, 41, 7, 5, 28],
    [46, 23, 34, 36, 22, 11, 3],
    [15, 39, 8, 13, 25, 24, 42],
    [32, 12, 18, 9, 10, 21, 0],
    [40, 47, 31, 35, 20, 26, 43]
]

start = time.time_ns()
sb = SlidingBoard(puzzle_10)  # puzzle_10
rec_seeker_counter = 0
print(k := sb.solve_puzzle())
print(35 in k)
print(98 in k)
print(f'counter: {rec_seeker_counter}')
finish = time.time_ns()
print(f'time elapsed: {(finish - start) // 10 ** 6} milliseconds')
# print(None or 98)
# print(sb.sliding_board)
# print(sb.solved_board)
# g = sb.sliding_board[0][0]
# print(g)
# sb.sliding_board[0][0].num = 98
# print(g)
# print(sb.locate_cell(5))
# print((n := sb.find_number_cell(99)).j, n.i)
# print(n.calc_manhattan_distance(sb.find_number_cell(86)))
