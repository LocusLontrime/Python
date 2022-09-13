import time

import numpy as np
import queue

def slide_puzzle(array):
    puzzle = Puzzle(array)
    puzzle.solver()
    return puzzle.steps

class Puzzle:
    def __init__(self, array):
        self.puzzle = np.array(array, dtype=object)
        self.solved = np.zeros_like(self.puzzle, dtype=int)
        self.height, self.width = self.puzzle.shape
        self.steps = []

        for i, row in enumerate(self.puzzle):
            for j, value in enumerate(row):
                self.puzzle[i, j] = Case(value)
                self.puzzle[i, j].y, self.puzzle[i, j].x = i, j
                self.solved[i, j] = 1 + j + self.width * i
        self.solved[-1, -1] = 0

        # Create all paths
        for row in self.puzzle:
            [case.get_paths(self.puzzle) for case in row]
    def clear(self):
        [case.clear() for case in np.ravel(self.puzzle)]

    def solver(self):
        self.reduce_problem()
        self.solve()

    # Solve the reduced problem
    def solve(self):
        for i in range(24):
            print('lala')
            solution = self.puzzle[-3:, -3:].ravel().tolist()[:-1]
            solution = [s.value for s in solution]
            if sorted(solution) == solution:
                return True

            objective = self.find_number(0)
            if i < 12:
                if objective.y == self.height - 1 and objective.x == self.width - 1:
                    board_piece = self.puzzle[-2, -1]
                if objective.y == self.height - 2 and objective.x == self.width - 1:
                    board_piece = self.puzzle[-2, -2]
                if objective.y == self.height - 2 and objective.x == self.width - 2:
                    board_piece = self.puzzle[-1, -2]
                if objective.y == self.height - 1 and objective.x == self.width - 2:
                    board_piece = self.puzzle[-1, -1]
            if i >= 12:
                if objective.y == self.height - 1 and objective.x == self.width - 1:
                    board_piece = self.puzzle[-1, -2]
                if objective.y == self.height - 2 and objective.x == self.width - 1:
                    board_piece = self.puzzle[-1, -1]
                if objective.y == self.height - 2 and objective.x == self.width - 2:
                    board_piece = self.puzzle[-2, -1]
                if objective.y == self.height - 1 and objective.x == self.width - 2:
                    board_piece = self.puzzle[-2, -2]
            self.steps.append(board_piece.value)
            objective.swap(board_piece)
        self.steps = None

    # reduce the problem to a 2x2 grid
    def reduce_problem(self):
        for i in range(self.height - 2):
            helper = (self.puzzle[i + 1, -1], self.puzzle[i + 1, -2],
                      self.puzzle[i + 2, -1], self.puzzle[i + 2, -2])
            self.look_line(self.puzzle[i, :], self.solved[i, :], helper)

            helper = (self.puzzle[-1, i + 1], self.puzzle[-2, i + 1],
                      self.puzzle[-1, i + 2], self.puzzle[-2, i + 2])
            self.look_line(self.puzzle[i + 1:, i], self.solved[i + 1:, i], helper)

        return True

    # For a given line, how it should be
    def look_line(self, line, solutions, helper):
        for case, solution in zip(line[:-2], solutions[:-2]):
            self.solve_number(case, solution)

        self.solve_number(helper[2], solutions[-1], is_solved=False)
        self.solve_number(helper[3], solutions[-2], is_solved=False)

        self.solve_number(line[-1], solutions[-2], is_solved=False)
        self.solve_number(helper[0], solutions[-1], is_solved=False)

        if line[-2] != self.find_number(0):
            self.solve_number(helper[1], line[-2].value, ignore=[helper[0], line[-1]], is_solved=False)

        self.solve_number(line[-2], solutions[-2])
        self.solve_number(line[-1], solutions[-1])

        return True

    def solve_number(self, position, number, ignore=None, is_solved=True):
        while position.value != number:
            origin = self.find_number(0)
            # Find the number that should be at the position
            objective = self.find_number(number)

            # look for the best adjecent case, relative to the
            # current position
            adjacent = objective.best_adjacent(self.puzzle, position)

            # Find the shortest path
            path = origin.astar(self, adjacent, objective, ignore)

            # Make the move
            for one, two in zip(path, path[1:]):
                self.steps.append(two.value)
                one.swap(two)
            self.steps.append(objective.value)
            path[-1].swap(objective)
        if is_solved:
            position.is_solved = True
        return True

    def find_number(self, num):
        for row in self.puzzle:
            for node in row:
                if node.value == num:
                    return node
        return None


class Case():
    def __init__(self, value):
        self.value = value
        self.is_solved = False
        self.paths = []
        self.distance = np.Infinity
        self.back = None

    def __gt__(self, other):
        return self.distance > other.distance

    def __repr__(self):
        return str(self.value)

    def clear(self):
        self.distance = np.Infinity
        self.back = None

    def distance_to(self, other):
        return abs(self.y - other.y) + abs(self.x - other.x)

    def swap(self, other):
        self.value, other.value = other.value, self.value
        self.is_solved, other.is_solved = other.is_solved, self.is_solved

    def get_paths(self, puzzle):
        height, width = puzzle.shape
        if self.y > 0:
            self.paths.append(puzzle[self.y - 1, self.x])
        if self.y < height - 1:
            self.paths.append(puzzle[self.y + 1, self.x])
        if self.x > 0:
            self.paths.append(puzzle[self.y, self.x - 1])
        if self.x < width - 1:
            self.paths.append(puzzle[self.y, self.x + 1])

    def best_adjacent(self, puzzle, relative):
        possible_paths = []

        for path in self.paths:
            if not path.is_solved:
                possible_paths.append((relative.distance_to(path), path))

        if not possible_paths:
            # Error in the solution
            print(puzzle)

        solution = sorted(possible_paths, key=lambda x: x[0])[0]
        return solution[1]

    def astar(self, puzzle, objective, number, ignore=None):
        ignore = ignore or []

        queuee = queue.PriorityQueue()
        self.distance = 0
        queuee.put((0, self))

        while not queuee.empty():
            _, case = queuee.get()
            if case == objective:
                break

            for pos_b in case.paths:
                if pos_b.back != case:
                    if pos_b != number and not pos_b.is_solved and pos_b not in ignore:
                        if pos_b.distance > 1 + case.distance:
                            pos_b.distance = 1 + case.distance
                            pos_b.back = case
                            queuee.put((pos_b.distance_to(objective), pos_b))

        node = objective
        path = []

        while node.back:
            path.append(node)
            node = node.back
        path.append(node)

        puzzle.clear()
        # print(f'part of path: {list(reversed(path))}')
        return list(reversed(path))

simple_example = [
    [1, 11, 3, 4, 16],
    [5, 13, 6, 8, 23],
    [9, 10, 7, 0, 17],
    [2, 14, 15, 12, 22],
    [19, 18, 20, 21, 24]
]
ex = [
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
# print(slide_puzzle(simple_example))
start = time.time_ns()
print(slide_puzzle(ex))
finish = time.time_ns()
print(f'time elapsed: {(finish - start) // 10 ** 6} milliseconds')
