# accepted on coderun
import sys
from collections import deque as dq

djdi = ((-1, 0), (0, 1), (1, 0), (0, -1))
letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'


class Sizes:
    def __init__(self, luh: int = 0, luw: int = 0, rbh: int = 0, rbw: int = 0):
        self.luh = luh
        self.luw = luw
        self.rbh = rbh
        self.rbw = rbw

    def __eq__(self, other: 'Sizes'):
        if isinstance(other, str):
            return False
        return self.luh == other.luh and self.luw == other.luw and self.rbh == other.rbh and self.rbw == other.rbw

    def __str__(self):
        return f'[{self.luh}, {self.luw}] [{self.rbh}, {self.rbw}]'

    def __repr__(self):
        return str(self)


def process_queries():
    m_rows, m_cols, ascii_table, row, heights, col, widths, q, queries = get_pars()
    print(f'LALA')
    # pre-calculation of the partial sums:
    partial_sums_heights = calc_partial_sums(heights)
    partial_sums_widths = calc_partial_sums(widths)
    # table:
    table = [[None for _ in range(col)] for _ in range(row)]
    # now let's process the ascii-table:
    process_table(ascii_table, table, m_rows, m_cols, row, heights, col, widths, partial_sums_heights,
                  partial_sums_widths)
    ascii_table = [[' ' if isinstance(t := ascii_table[j][i], Sizes) else t for i in range(m_cols)] for j in
                   range(m_rows)]
    # the main cycle:
    for query in queries:
        if query[0] == 'merge':
            flag = merge_cells_table(ascii_table, table, m_rows, m_cols, query[1], query[2], heights, widths, partial_sums_heights, partial_sums_widths)
            if flag:
                print_ascii_table(ascii_table)
        else:
            flag = split(ascii_table, table, m_rows, m_cols, query[1], heights, widths, partial_sums_heights, partial_sums_widths)
            if flag:
                print_ascii_table(ascii_table)


def translate(cell: str) -> tuple[int, int]:
    i_ = sum(1 for _ in cell if _.isalpha())
    column = cell[:i_]
    row = cell[i_:]
    return int(row) - 1, sum((ord(s) - 64) * 26 ** i for i, s in enumerate(reversed(column))) - 1


def process_table(ascii_table: list[list[str]], table: list, m_rows, m_cols, row: int, heights: list[int],
                  col: int, widths: list[int], psh: list[int], psw: list[int]):
    ascii_j_ = 1
    for j_ in range(row):
        ascii_i_ = 1
        for i_ in range(col):
            if ascii_table[ascii_j_][ascii_i_] == ' ':
                # starting bfs:
                bfs(ascii_table, m_rows, m_cols, ascii_j_, ascii_i_, j_, i_, psh, psw)
            # building a table:
            table[j_][i_] = ascii_table[ascii_j_][ascii_i_]
            ascii_i_ += widths[i_] + 1
        ascii_j_ += heights[j_] + 1


def bfs(ascii_table: list[list[str]], m_rows: int, m_cols: int, start_j: int, start_i: int, j: int, i: int,
        partial_sums_heights: list[int], partial_sums_widths: list[int]):
    sizes = Sizes(j, i, 0, 0)
    deq = dq()
    deq.appendleft((start_j, start_i))
    while deq:
        _j, _i = deq.pop()
        # visiting the cell:
        if ascii_table[_j][_i] == ' ':
            sizes.rbh = max(sizes.rbh, _j)
            sizes.rbw = max(sizes.rbw, _i)
            ascii_table[_j][_i] = sizes
            # getting the cell's neighs:
            for dj, di in djdi:
                j_, i_ = _j + dj, _i + di
                if 0 <= j_ < m_rows and 0 <= i_ < m_cols:
                    deq.appendleft((j_, i_))
    sizes.rbh = partial_sums_heights.index(sizes.rbh)
    sizes.rbw = partial_sums_widths.index(sizes.rbw)


def calc_partial_sums(array: list[int]) -> list[int]:
    partial_sums_arr = [0 for _ in range(len(array))]
    partial_sums_arr[0] = array[0]
    for i in range(1, len(array)):
        partial_sums_arr[i] = partial_sums_arr[i - 1] + array[i] + 1
    return partial_sums_arr


def merge_cells_table(ascii_table: list[list[str]], table: list[list[Sizes]], m_rows: int, m_cols: int, cell1: str, cell2: str,
                      heights: list[int], widths: list[int], psh: list[int], psw: list[int]) -> bool:
    cell1 = translate(cell1)
    cell2 = translate(cell2)
    cell1_sizes = table[cell1[0]][cell1[1]]
    cell2_sizes = table[cell2[0]][cell2[1]]
    if cell1_sizes == cell2_sizes:
        print(f'Can not merge cell with itself')
        return False
    elif cell1_sizes.luh == cell2_sizes.luh and cell1_sizes.rbh == cell2_sizes.rbh and min(cell1_sizes.rbw, cell2_sizes.rbw) + 1 == max(cell1_sizes.luw, cell2_sizes.luw):
        # horizontal alignment:
        print(f'Merged horizontally-aligned cells')
        new_sizes = Sizes(cell1_sizes.luh, min(cell1_sizes.luw, cell2_sizes.luw), cell1_sizes.rbh,
                          max(cell1_sizes.rbw, cell2_sizes.rbw))
        # ascii-table changing:
        i_const = psw[min(cell1_sizes.rbw, cell2_sizes.rbw)] + 1
        for ascii_j_ in range(jb := psh[cell1_sizes.luh] - heights[cell1_sizes.luh] + 1, (je := psh[cell1_sizes.rbh]) + 1):
            ascii_table[ascii_j_][i_const] = ' '
        # crosses updating:
        if jb - 2 < 0 or ascii_table[jb - 2][i_const] == ' ':
            ascii_table[jb - 1][i_const] = '-'
        if je + 2 >= m_rows or ascii_table[je + 2][i_const] == ' ':
            ascii_table[je + 1][i_const] = '-'
    elif cell1_sizes.luw == cell2_sizes.luw and cell1_sizes.rbw == cell2_sizes.rbw and min(cell1_sizes.rbh, cell2_sizes.rbh) + 1 == max(cell1_sizes.luh, cell2_sizes.luh):
        # vertical alignment:
        print(f'Merged vertically-aligned cells')
        new_sizes = Sizes(min(cell1_sizes.luh, cell2_sizes.luh), cell1_sizes.luw, max(cell1_sizes.rbh, cell2_sizes.rbh),
                          cell1_sizes.rbw)
        # ascii-table changing:
        j_const = psh[min(cell1_sizes.rbh, cell2_sizes.rbh)] + 1
        for ascii_i_ in range(ib := psw[cell1_sizes.luw] - widths[cell1_sizes.luw] + 1, (ie := psw[cell1_sizes.rbw]) + 1):
            ascii_table[j_const][ascii_i_] = ' '
        # crosses updating:
        if ib - 2 < 0 or ascii_table[j_const][ib - 2] == ' ':
            ascii_table[j_const][ib - 1] = '|'
        if ie + 2 >= m_cols or ascii_table[j_const][ie + 2] == ' ':
            ascii_table[j_const][ie + 1] = '|'
    else:
        # no alignment is possible:
        print(f'Can not merge unaligned cells')                                       # 36.6 98
        return False
    for j_ in range(new_sizes.luh, new_sizes.rbh + 1):
        for i_ in range(new_sizes.luw, new_sizes.rbw + 1):
            table[j_][i_] = new_sizes
    return True


def split(ascii_table: list[list[str]], table: list[list[Sizes]], m_rows: int, m_cols: int, cell: str, heights: list[int], widths: list[int],
          psh: list[int], psw: list[int]):
    cell = translate(cell)
    cell_sizes = table[cell[0]][cell[1]]
    if cell_sizes.luh == cell_sizes.rbh and cell_sizes.luw == cell_sizes.rbw:
        # the cell is already an elementary one:
        print(f'Can not split elementary cell')
        # raise ValueError(f'Can not split elementary cell')
        return False
    # changing the ascii-table:
    # a. -->> new horizontal lines:
    for i_ in range(cell_sizes.luw, cell_sizes.rbw):
        ascii_i_ = psw[i_] + 1
        for ascii_j_ in range(jb := psh[cell_sizes.luh] - heights[cell_sizes.luh] + 1, (je := psh[cell_sizes.rbh]) + 1):
            ascii_table[ascii_j_][ascii_i_] = '|'
        # crosses adding:
        if jb - 1 >= 0:
            ascii_table[jb - 1][ascii_i_] = '+'
        if je + 1 < m_rows:
            ascii_table[je + 1][ascii_i_] = '+'
    # b. -->> new vertical ones:
    for j_ in range(cell_sizes.luh, cell_sizes.rbh):
        ascii_j_ = psh[j_] + 1
        for ascii_i_ in range(ib := psw[cell_sizes.luw] - widths[cell_sizes.luw] + 1, (ie := psw[cell_sizes.rbw]) + 1):
            if ascii_table[ascii_j_][ascii_i_] == '|':
                ascii_table[ascii_j_][ascii_i_] = '+'
            else:
                ascii_table[ascii_j_][ascii_i_] = '-'
        # crosses adding:
        if ib - 1 >= 0:
            ascii_table[ascii_j_][ib - 1] = '+'
        if ie + 1 < m_cols:
            ascii_table[ascii_j_][ie + 1] = '+'
    # splitting onto elementary cells:
    for j_ in range(cell_sizes.luh, cell_sizes.rbh + 1):
        for i_ in range(cell_sizes.luw, cell_sizes.rbw + 1):
            table[j_][i_] = Sizes(j_, i_, j_, i_)
    print(f'Split onto {(cell_sizes.rbh - cell_sizes.luh + 1) * (cell_sizes.rbw - cell_sizes.luw + 1)} cells')
    return True


def print_ascii_table(ascii_table: list[list[str]]):
    ascii_t = "\n".join(''.join(row) for row in ascii_table)
    print(f'{ascii_t}')


def get_pars():
    m_rows, m_cols = map(int, input().split())
    ascii_table = [[_ for _ in input()] for _ in range(m_rows)]
    row = int(input())
    heights = [int(_) for _ in input().split()]
    col = int(input())
    widths = [int(_) for _ in input().split()]
    q = int(input())
    queries = [input().split() for _ in range(q)]
    return m_rows, m_cols, ascii_table, row, heights, col, widths, q, queries  # 36.6 98


process_queries()

# print(f't: {translate(f"ABB117")}')


# print(f'{ord("A")}')

ascii_table_ = \
    """+--+------+-------------+
       |  |      |             |
       |  |      |             |
       +--+----+-+-------+-----+
       |       | |       |     |
       |       | |       |     |
       |       | |       |     |
       +-------+-+-------+-----+"""                                                   # 36.6 98

# 8 25
# +--+------+-------------+
# |  |      |             |
# |  |      |             |
# +--+----+-+-------+-----+
# |       | |       |     |
# |       | |       |     |
# |       | |       |     |
# +-------+-+-------+-----+
# 2
# 2 3
# 5
# 2 4 1 7 5
# 0
