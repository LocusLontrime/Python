
def solve_puzzle(clues: tuple):
    dim = 4
    puzzle = [[0] * dim for _ in range(dim)]

    skyscrapers_used_horizontally = [[] * dim]
    skyscrapers_used_vertically = [[] * dim]

    def rec_backtracking(j: int, i: int):

        if j == dim and i == 0:
            return puzzle

        right_ones = [0] * dim
        directions = [[0, j + 1, 1, i], [i, 0 - 1, -1, j], [j, 0 - 1, -1, i], [0, i + 1, 1, j]]

        for sk in skyscrapers_used_horizontally:
            pass

        for sk in skyscrapers_used_vertically:
            pass

        for dir_ind in range(len(directions)):
            curr_max = 0
            for k in range(directions[dir_ind][0], directions[dir_ind][1], directions[dir_ind][2]):
                element = puzzle[k][directions[dir_ind][3]] if dir_ind in [0, 2] else puzzle[directions[dir_ind][3]][k]
                if element > curr_max:
                    right_ones[dir_ind] += 1
                    curr_max = element

        if right_ones[0] + dim - 1 - j < clues[i] or right_ones[1] + dim - 1 - i < clues[4 + j] or right_ones[2] + dim - 1 - j < clues[8 + (dim - 1 - i)] or right_ones[3] + dim - 1 - i < clues[12 + (dim - 1 - j)]:
            pass
        else:
            if i == dim - 1:
                rec_backtracking(j + 1, i)
            else:
                rec_backtracking(j, i + 1)

    rec_backtracking(0, 0)








