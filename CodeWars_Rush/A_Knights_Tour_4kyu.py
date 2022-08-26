# accepted on codewars.com
import sys

deltas = [[-2, -1, 1, 2, 2, 1, -1, -2], [1, 2, 2, 1, -1, -2, -2, -1]]
order = [4, 0, 5, 1, 6, 2, 7, 3]
adjOnes = [[-1, 0, 1, 0], [0, 1, 0, -1]]
flag: bool
coordinates_of_knight: list[list[int]]


def knights_tour(start: tuple[int, int], size: int):
    global flag, coordinates_of_knight

    board = [[0] * size for _ in range(size)]
    flag = True

    board[start[0]][start[1]] = 1

    coordinates_of_knight = [start]

    # checks coordinates if they are located inside the board
    def is_valid(board_size: int, j: int, i: int) -> bool:
        return 0 <= i < board_size and 0 <= j < board_size

    def next_possible_cells(curr_j: int, curr_i: int) -> int:  # both these methods can be simplified to one method,
        # but let them be in order to achieve a greater understandability
        nextPossibleCells = 0

        for i in range(0, len(deltas[0])):
            if is_valid(size, curr_j + deltas[0][i], curr_i + deltas[1][i]) and board[curr_j + deltas[0][i]][curr_i + deltas[1][i]] == 0:
                nextPossibleCells += 1

        return nextPossibleCells

    def adjacent_possible_cells(curr_j: int, curr_i: int):
        adjacentPossibleCells = 0

        for i in range(0, len(adjOnes[0])):
            if is_valid(size, curr_j + adjOnes[0][i], curr_i + adjOnes[1][i]) and board[curr_j + adjOnes[0][i]][curr_i + adjOnes[1][i]] == 0:
                adjacentPossibleCells += 1

        return adjacentPossibleCells

    # linear recursion with Warnsdorf's heuristic, adj and angle minimization ath the every step and backtracking
    def recursive_seeker(j: int, i: int, counter: int) -> None:  # works better, but cannot handle really big sizes...
        global flag, coordinates_of_knight

        # needs to be run with special parameters
        if counter == size * size + 1:
            flag = False
            return

        allPossibleCells = dict()
        for index in range(0, len(deltas[0])):
            if is_valid(size, j + deltas[0][index], i + deltas[1][index]) and board[j + deltas[0][index]][i + deltas[1][index]] == 0:
                allPossibleCells[index] = next_possible_cells(j + deltas[0][index], i + deltas[1][index])

        if len(allPossibleCells) > 0:

            minValueNext = len(deltas[0])
            minValueAdj = len(adjOnes[0])
            minAngleKey: int

            for key in allPossibleCells.keys():
                if allPossibleCells.get(key) < minValueNext:
                    minValueNext = allPossibleCells.get(key)

            minNextPossCells = dict()

            for key in allPossibleCells.keys():
                if allPossibleCells.get(key) == minValueNext:
                    minNextPossCells[key] = adjacent_possible_cells(j + deltas[0][key], i + deltas[1][key])

            for key in minNextPossCells.keys():
                if minNextPossCells.get(key) < minValueAdj:
                    minValueAdj = minNextPossCells.get(key)

            minNextPossAdjCells = dict()

            for key in minNextPossCells.keys():
                if minNextPossCells.get(key) == minValueAdj:
                    minNextPossAdjCells[key] = minNextPossCells[key]

            for k in range(0, len(order)):
                if flag and order[k] in minNextPossAdjCells.keys():
                    minAngleKey = order[k]

                    board[j + deltas[0][minAngleKey]][i + deltas[1][minAngleKey]] = counter
                    coordinates_of_knight.append((j + deltas[0][minAngleKey], i + deltas[1][minAngleKey]))
                    recursive_seeker(j + deltas[0][minAngleKey], i + deltas[1][minAngleKey], counter + 1)
                    if flag:
                        board[j + deltas[0][minAngleKey]][i + deltas[1][minAngleKey]] = 0
                        coordinates_of_knight = coordinates_of_knight[:-1]

    recursive_seeker(start[0], start[1], 1 + 1)

    for arr in board:
        print(arr)

    print()

    print(f'length: {len(coordinates_of_knight)}')

    return coordinates_of_knight


# print(knights_tour([0, 0], 10))

sys.setrecursionlimit(1000000)

print(knights_tour((0, 0), 43))

# print([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11][:-1])










