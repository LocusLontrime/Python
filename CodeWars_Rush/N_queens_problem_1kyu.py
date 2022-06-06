flag_of_rec_stop = False


def total_n_queens(n: int):

    placements = list()

    def recursive_seeker(row: int, vertical_set: list[int],  # List -> only for printing the placements queens coordinates
                         diag1_set: set[int], diag2_set: set[int],
                         board_size: int) -> None:
        global flag_of_rec_stop

        if flag_of_rec_stop:
            return

        if row == board_size:
            curr_set = set()
            currRow = 0

            for i in vertical_set:
                curr_set.add((currRow, i))
                currRow += 1

            placements.extend(curr_set)

            flag_of_rec_stop = True

            return

        for i in range(board_size):

            if i not in vertical_set and row + i not in diag1_set and row - i not in diag2_set:
                newVerticalSet = list(vertical_set)
                newDiag1Set = set(diag1_set)
                newDiag2Set = set(diag2_set)

                newVerticalSet.append(i)
                newDiag1Set.add(row + i)
                newDiag2Set.add(row - i)

                recursive_seeker(row + 1, newVerticalSet, newDiag1Set, newDiag2Set, board_size)

    recursive_seeker(0, [], set(), set(), n)

    return placements if len(placements) > 0 else None


print(f'All placements number: {total_n_queens(25)}', end='\n\n')

