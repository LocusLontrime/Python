def solve(clues_):  # 36 366 98 989 LL
    """solves the nonogram given"""
    ...

    def rec_line_solver():
        ...

    ...


def solve_line(line: list[int], line_clues: tuple[int, ...]) -> dict[int, int]:
    """finds all the necessary 1s and 0s for the lines given and its clues"""
    length = len(line)
    size = len(line_clues)
    # dictionary for necessaries:
    necessaries: dict[int, int] = dict()
    ...

    def rec_seeker():
        ...

    rec_seeker()

    ...
    return necessaries


clues = (
    (
        (4, 3), (1, 6, 2), (1, 2, 2, 1, 1), (1, 2, 2, 1, 2), (3, 2, 3),
        (2, 1, 3), (1, 1, 1), (2, 1, 4, 1), (1, 1, 1, 1, 2), (1, 4, 2),
        (1, 1, 2, 1), (2, 7, 1), (2, 1, 1, 2), (1, 2, 1), (3, 3)
    ), (
        (3, 2), (1, 1, 1, 1), (1, 2, 1, 2), (1, 2, 1, 1, 3), (1, 1, 2, 1),
        (2, 3, 1, 2), (9, 3), (2, 3), (1, 2), (1, 1, 1, 1),
        (1, 4, 1), (1, 2, 2, 2), (1, 1, 1, 1, 1, 1, 2), (2, 1, 1, 2, 1, 1), (3, 4, 3, 1)
    )
)

solve(clues)


import sys
sys.path.append('')
