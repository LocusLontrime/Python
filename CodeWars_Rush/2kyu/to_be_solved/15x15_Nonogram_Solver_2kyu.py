filled_square = f'*'


lines: list['Line']


class Line:
    def __init__(self, index: int, start: int, end: int, clues: list[int], is_row: bool = True):
        self.ind = index
        self.st = start  # <<-- included
        self.en = end   # <<-- excluded
        self.clues = clues
        self.row = is_row

    def process(self, board: list[list[str]]):
        print(f'processing line: {self}')
        # smart search:
        for pivot_i, clue in enumerate(self.clues):
            # find leftmost and rightmost placements for this group of squares and if they match then the clue is done:
            # 1. leftmost part:
            print(f'    pivot_i, CLUE: {pivot_i, clue}')
            clue_i, line_i = 0, self.st
            print(f'        leftmost part processing...')
            while clue_i < pivot_i:
                line_i = self.place_clue(clue_i, line_i, board, left=True)
                print(f'            clue_i, line_i: {clue_i, line_i}')
                clue_i += 1
            leftmost_border = line_i
            # 2. rightmost part:
            print(f'        rightmost part processing...')
            clue_i, line_i = len(self.clues) - 1, self.en - 1
            while clue_i > pivot_i:
                line_i = self.place_clue(clue_i, line_i, board, left=False)
                print(f'            clue_i, line_i: {clue_i, line_i}')
                clue_i -= 1
            rightmost_border = line_i
            print(f'leftmost_border, rightmost_border: {leftmost_border, rightmost_border}')
            # analysing:
            if (gap := rightmost_border - leftmost_border + 1) == clue:
                # division into 2 parts (left and right):
                print(f'DIVISION --------------->>>>>>>>>>>>>>>>')
                self.divide(pivot_i, leftmost_border, rightmost_border, board)
                return
            else:
                # filling squares:
                print(f'SQUARES FULFILLING >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
                if 2 * clue > gap:
                    nq = 2 * clue - gap
                    delta = gap - clue
                    for i in range(leftmost_border + delta, leftmost_border + delta + nq):
                        if self.get_board(self.ind, i, board) != '1':
                            self.set_board(self.ind, i, '1', board)

        # TODO: 1. после размещения правых или левых clues стоит проверять дальнейшую ситуацию для возможного сужения интервала и активации фаза деления.
        # TODO: 2. проверять крайние единицы на возможное фиксированное (board[j][0 or mi - 1] and board[0 or mj - 1][i]) заполнение и уменьшения листа clues на единицу -> деление.
        # TODO: 3. проверять недосягаемые области!!!

    def coords(self, j: int, i: int) -> tuple[int, int]:
        return (j, i) if self.row else (i, j)

    def is_valid(self, index: int) -> bool:
        return self.st <= index < self.en

    def get_board(self, j: int, i: int, board: list[list[str]]) -> str:
        j_, i_ = self.coords(j, i)
        return board[j_][i_]

    def set_board(self, j: int, i: int, val: str, board: list[list[str]]) -> None:
        j_, i_ = self.coords(j, i)
        board[j_][i_] = val

    def place_clue(self, clue_i: int, line_i: int, board: list[list[str]], left: bool = True) -> int:
        clue_i_, line_i_ = clue_i, line_i
        di = 1 if left else -1
        while self.is_valid(line_i_) and self.get_board(self.ind, line_i_, board) in ['-1', '1'] and abs(line_i_ - line_i) < self.clues[clue_i]:
            line_i_ += di
        print(f'                placing clue, line_i: {line_i} | delta, clue: {abs(line_i_ - line_i), self.clues[clue_i]}')
        if abs(line_i_ - line_i) == self.clues[clue_i]:
            if not self.is_valid(line_i_) or self.get_board(self.ind, line_i_, board) != '1':
                print(f'.......................................................................')
                return line_i_ + di
        return self.place_clue(clue_i, line_i + di, board, left)

    def divide(self, clue_i: int, lb: int, rb: int, board: list[list[str]]) -> list['Line']:
        global lines
        lines.remove(self)
        # 1st case, no clues left:
        if len(self.clues) == 1:
            new_lines = []
        # 2nd case, only leftmost clues left
        elif clue_i == len(self.clues) - 1:
            new_lines = [Line(self.ind, self.st, lb - 2, self.clues[: clue_i])]
        # 3rd case, only rightmost clues left:
        elif clue_i == 0:
            new_lines = [Line(self.ind, rb + 2, self.en, self.clues[clue_i + 1:])]
        # 4th case, both leftmost and rightmost clues left:
        else:
            left_line, right_line = Line(self.ind, self.st, lb - 2, self.clues[: clue_i]), Line(self.ind, rb + 2, self.en, self.clues[clue_i + 1:])
            new_lines = [left_line, right_line]
        lines += new_lines
        # processing new lines:
        for new_line in new_lines:
            new_line.process(board)
        # returning new lines:
        return new_lines

    # ???
    def __hash__(self):
        ...

    # ???
    def __lt__(self, other):
        ...

    def __str__(self):
        type_ = 'row' if self.row else 'col'
        return f'{type_}: [{self.ind}]({self.st},{self.en}), clues: {self.clues}'

    def __repr__(self):
        ...


def solve(clues: tuple):
    global lines
    lines = []
    column_clues, row_clues = clues
    mj, mi = len(row_clues), len(column_clues)
    board = [['-1' for _ in range(mi)] for _ in range(mj)]
    # first move, rows and columns line solving:
    for j, row_clue in enumerate(row_clues):
        lines.append(Line(j, 0, mi, row_clue, is_row=True))
    for i, column_clue in enumerate(column_clues):
        lines.append(Line(i, 0, mj, column_clue, is_row=False))
    # processing the lines:
    ind = 0
    for line in lines:
        ind += 1
        print(f'{ind}. ', end='')
        line.process(board)
    # printing board:
    print(f'RESULT: ')
    for row in board:
        r = ''.join(['_' if ch == '-1' else '*' for ch in row])
        print(f'{r}')
    # lines:
    print(f'LINES: ')
    for i, line in enumerate(lines):
        print(f'{i}. {line}')
    # next step:
    cols = zip(*board)
    print(f'COLS: ')
    for col in cols:
        print(f'{col}')


def solve_line(index: int, length: int, line_clues: tuple[int, ...], board: list[list[str]], rows: bool = True) -> dict[int, int]:  # line: list[int]
    """finds all the necessary 1s and 0s for the lines given and its clues"""
    # length = len(line)
    size = len(line_clues)
    print(f'{index}th {("row" if rows else "column")} clues: {line_clues}, length: {length}')
    # some logic with ones and crosses given:
    ...  # ???
    # dictionary for necessaries:
    necessaries: dict[int, int] = dict()
    # cycling all over the clues:
    squares_filled = 0
    for i, clue in enumerate(line_clues):
        ls, rs = sum(line_clues[:i]) + i, sum(line_clues[i + 1:]) + size - i - 1
        gap = length - ls - rs
        if 2 * clue > gap:
            nq = 2 * clue - gap
            squares_filled += nq
            delta = gap - clue
            for ind in range(nq):
                necessaries[ls + delta + ind] = 1
                # board changing:
                if rows:
                    board[index][ls + delta + ind] = '1'
                else:
                    board[ls + delta + ind][index] = '1'
    if squares_filled == sum(line_clues):
        print(f'{index}{"th "}{("row" if rows else "column")}{" been fully filled"}')
    string = [filled_square if i in necessaries.keys() else '_' for i in range(length)]
    string = ''.join(string)
    print(f'string: {string}')
    return necessaries


def resolve_line(index: int, length: int, line_clues: tuple[int, ...], board: list[list[str]], rows: bool = True) -> None:
    ...


def smart_solve(board: list[list[str]]):
    ...


clues_ = (
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

solve(clues_)

# print(f'necessaries: {solve_line(9, (3, 4))}')

