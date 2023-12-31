import math
import time
from typing import Any

hor = {(0, 1), (0, -1)}
ver = {(1, 0), (-1, 0)}
diags = {(j, i) for j in [1, -1] for i in [1, -1]}
hv_neighs = hor | ver
hvd_neighs = hv_neighs | diags


def break_evil_pieces(shape: str) -> list[str]:
    # base case of no shapes:
    print(f'shape:\n{shape}')
    interim_res = simplify(shape)
    if interim_res is None:
        return []
    smj, smi, simplified_shape = interim_res
    empty_cells: set[tuple[int, int]] = {(j, i) for j in range(smj) for i in range(smi) if
                                         simplified_shape[j][i] == ' '}
    print(f'{len(empty_cells)} empty_cells: {empty_cells}')
    # core cycle:
    figures = []
    while empty_cells:
        # processing the figures:
        arbitrary_empty_cell = empty_cells.pop()
        print(f'arbitrary_empty_cell: {arbitrary_empty_cell}')
        figure_empties: set[tuple[int, int]] = {arbitrary_empty_cell}
        front_neighs: set[tuple[int, int]] = {arbitrary_empty_cell}
        # finding all the empty cells for the current figure:
        while front_neighs:
            front_neighs = {(j, i) for coords in front_neighs for j, i in get_neighs(*coords, hv_neighs) if
                            (j, i) in empty_cells and (j, i) not in figure_empties}
            print(f'front_neighs: {front_neighs}')
            figure_empties |= front_neighs
        print(f'{len(figure_empties)} figure_empties: {figure_empties}')
        # updating overall empty cells:
        empty_cells -= figure_empties
        # defining the outer and inner figure's borders:
        borders = {(j, i) for coords in figure_empties for j, i in get_neighs(*coords, hvd_neighs) if
                   (j, i) not in figure_empties}
        print(f'{len(borders)} border cells: {borders}')
        # defining min/max j and i for the current figure:
        min_j, min_i, max_j, max_i = math.inf, math.inf, 0, 0
        for j, i in borders:
            print(f'j, i: {j, i}')
            min_j = min(min_j, j)
            max_j = max(max_j, j)
            min_i = min(min_i, i)
            max_i = max(max_i, i)
        print(f'min_j, min_i, max_j, max_i: {min_j, min_i, max_j, max_i}')
        if min_j < 0 or min_i < 0 or max_j > smj - 1 or max_i > smi - 1:
            continue
        # extracting figure from the simplified_shape:
        figure = [row[min_i: max_i + 1] for row in simplified_shape[min_j: max_j + 1]]
        fmj, fmi = len(figure), len(figure[0])
        print(f'fmj, fmi: {fmj, fmi}')
        print(f'figure: ')
        for row in figure:
            print(f'{row}')
        # removing the excess '+'s and all the inner cells for the inner-bound:
        for j in range(fmj):
            for i in range(fmi):
                # we cannot leave any non-space cells inside the inner board:
                j_, i_ = j + min_j, i + min_i
                if figure[j][i] != ' ' and (j_, i_) not in borders:
                    figure[j][i] = ' '
                elif figure[j][i] == '+':
                    print(f'+ found; j, i: {j, i}')
                    f1 = (vneighs := get_neighs(j_, i_, ver)).issubset(borders)
                    f2 = (hneighs := get_neighs(j_, i_, hor)).issubset(borders)
                    print(f'...vneighs: {vneighs}')
                    print(f'...hneighs: {hneighs}')
                    print(f'...f1, f2: {f1, f2}')
                    if f1 or f2:
                        ver_symbs = {simplified_shape[nj][ni] for nj, ni in vneighs if (nj, ni) in borders}
                        hor_symbs = {simplified_shape[nj][ni] for nj, ni in hneighs if (nj, ni) in borders}
                        print(f'...ver_symbs: {ver_symbs}')
                        print(f'...hor_symbs: {hor_symbs}')
                        if f1 and not f2 and ver_symbs == {'|'} and '-' not in hor_symbs:
                            figure[j][i] = '|'
                        elif f2 and not f1 and hor_symbs == {'-'} and '|' not in ver_symbs:
                            figure[j][i] = '-'
        print(f'figure purified: ')
        for row in figure:
            print(f'{row}')
        # reshaping figure to the initial form:
        figure = [[el for el in row[::2]] for row in figure[::2]]
        print(f'figure reshaped: ')
        for row in figure:
            print(f'{row}')
        figure = '\n'.join(eliminate_right_spaces(''.join(el for el in row)) for row in figure)
        print(f'str figure:')
        print(f'{figure}')
        figures.append(figure)

    # print(f'empty cells remained: {empty_cells}')
    return figures


def eliminate_right_spaces(string: str) -> str:
    i = len(string) - 1
    while string[i] == ' ':
        i -= 1
    return string[:i + 1]


def get_neighs(j: int, i: int, links: set[tuple[int, int]]):
    return {(j + dj, i + di) for dj, di in links}


def simplify(shape: str) -> tuple[int, int, Any]:
    shape = shape.split('\n')
    print(f'pre board: ')
    for row in shape:
        print(f'{row}')
    # eliminating unnecessary spaces, cutting off the shape:
    while not set(shape[0]) or set(shape[0]) == {' '}:
        shape = shape[1:]
        if not shape:
            return None
    while not set(shape[-1]) or set(shape[-1]) == {' '}:
        shape = shape[:-1]
    mj, mi = len(shape), 0
    print(f'board: ')
    for row in shape:
        print(f'{row}')
    # rectanglifying the shape:
    for row in shape:
        mi = max(mi, len(row))
    for i, row in enumerate(shape):
        shape[i] += ' ' * (mi - len(row))
    print(f'rectanglified board: ')
    for row in shape:
        print(f'{row}')
    # simplifying the shape:
    smj = 2 * mj - 1
    smi = 2 * mi - 1
    simplified_shape = [[' ' for _ in range(smi)] for _ in range(smj)]
    for j in range(smj):
        if j % 2:
            col_links = {'+', '|'}
            for i in range(mi):
                if shape[j_ := j // 2][i] in col_links and shape[j_ + 1][i] in col_links:
                    simplified_shape[j][2 * i] = '|'
        else:
            row_links = {'+', '-'}
            for i in range(smi):
                if i % 2:
                    if shape[j_ := j // 2][i_ := i // 2] in row_links and shape[j_][i_ + 1] in row_links:
                        simplified_shape[j][i] = '-'
                else:
                    simplified_shape[j][i] = shape[j // 2][i // 2]
    print(f'smj, smi: {smj, smi}')
    print(f'simplified board: ')
    for row in simplified_shape:
        print(f'{row}')
    return smj, smi, simplified_shape


ex = f'\n' \
     f'+--+---------+\n' \
     f'|  |         |\n' \
     f'|  +---+     |\n' \
     f'|      |     |\n' \
     f'+------+-----+\n' \
     f'|      |     |\n' \
     f'|      |     |\n' \
     f'+------+-----+'

ex_x = f'\n' \
       f'++-------+\n' \
       f'||   +--+|\n' \
       f'|++  |  ||\n' \
       f'| |  +--+|\n' \
       f'+-+-+----+\n' \
       f'| | |    |\n' \
       f'| | |    |\n' \
       f'+-+-+----+'

ex_z = f'\n' \
       f'+-------+ +----------+\n' \
       f'|       | |          |\n' \
       f'| +-+ +-+ +-+    +-+ |\n' \
       f'+-+ | |     |  +-+ +-+\n' \
       f'    | +-----+--+\n' \
       f'+-+ |          +-+ +-+\n' \
       f'| +-+  +----+    | | |\n' \
       f'| |    |    |    +-+ |\n' \
       f'| +----++ +-+        |\n' \
       f'|       | |          |\n' \
       f'+-------+ +----------+'

ex_w = f'\n' \
       f'+--------+-+----------------+-+--------+\n' \
       f'|        +-+                +-+        |\n' \
       f'|                                      |\n' \
       f'|                                      |\n' \
       f'|                                      |\n' \
       f'|                                      |\n' \
       f'++                 +-------------------+\n' \
       f'||                 |                   |\n' \
       f'++                 +------+     +------+\n' \
       f'|                         |     |      |\n' \
       f'|                         +-+ +-+      |\n' \
       f'|                           | |        |\n' \
       f'|                           | |        |\n' \
       f'|        +-+                | |        |\n' \
       f'|        +-+                +-+        |\n' \
       f'|  +-----+ |    ++                     |\n' \
       f'|  +-++----+    ++                     |\n' \
       f'|    ++                                |\n' \
       f'|    ||                                |\n' \
       f'++   |+-------------+                 ++\n' \
       f'||   |              |                 ||\n' \
       f'++   +---+ +--------+                 ++\n' \
       f'|        | |                           |\n' \
       f'|        | |                           |\n' \
       f'|        | |                           |\n' \
       f'|        | |                           |\n' \
       f'|        | |                +-+        |\n' \
       f'|        | |                +-+        |\n' \
       f'|        | |                           |\n' \
       f'|   +----+ |                           |\n' \
       f'|   |+-----+    ++                     |\n' \
       f'|   ||          ||         +----+      |\n' \
       f'++  ||  +-------+| ++      |+--+|  ++--+\n' \
       f'||  ||  |     +--+ ||      ||++||  ||  |\n' \
       f'++  ||  |     +---+++      ||++||  ++--+\n' \
       f'|   ||  +--------+|        |+--+|      |\n' \
       f'|   |+-----------+|        +----+      |\n' \
       f'|   +----+ +------+                    |\n' \
       f'|        | |                           |\n' \
       f'|        | |                +-+        |\n' \
       f'|        | |                | |        |\n' \
       f'|        | |                | |        |\n' \
       f'|  +-----+ |                | +-----+  |\n' \
       f'|  |+-+    |                |    +-+|  |\n' \
       f'|  || |  +-+                +-+  | ||  |\n' \
       f'+--+| +--+    +----------+    +--+ |+--+\n' \
       f'|   |      +--+          +--+      |   |\n' \
       f'+---+  +---+   +--------+   +---+  +---+\n' \
       f'|      |       |        |       |      |\n' \
       f'|      +-+ +---+        +---+ +-+      |\n' \
       f'|        | |                | |        |\n' \
       f'|        | |                | |        |\n' \
       f'|        | |                | |        |\n' \
       f'+--------+-+----------------+-+--------+'

ex_xxx = f'\n' \
         f'+--------+-+----------------+-+----------------+-+--------+\n' \
         f'|        +-+                | |                +-+        |\n' \
         f'|    +------+               ++++           +------+       |\n' \
         f'|    |+----+|               ++++           |+----+|       |\n' \
         f'|    ||+--+||               ++++           ||+--+||       |\n' \
         f'|    |||++|||               ++++           |||++|||       |\n' \
         f'++   |||++|||      +-----------+      ++   |||++|||      ++\n' \
         f'||   |||+-+||      | +--------+|      ||   |||+-+||      ||\n' \
         f'++   ||+---+|      +-+   +---+||      ++   ||+---+|      ++\n' \
         f'|    |+-++--+            |+-+|||           |+-++--+       |\n' \
         f'|+---+--+|               || ++||       +---+--+|          |\n' \
         f'|+-------+               |+---+|       +-------+          |\n' \
         f'|                        +-----+                          |\n' \
         f'|        +-+                +-+                +-+        |\n' \
         f'|        +-+                | |                | |        |\n' \
         f'|  +-----+ |    ++          | |                ++++       |\n' \
         f'|  +-++----+    ++     +----+ |                ++++       |\n' \
         f'|    ++                |+-----+    ++          ++++       |\n' \
         f'|    ||                ||          ||          ++++       |\n' \
         f'++   |+-------------+  ||  +-------+| +-----------+      ++\n' \
         f'||   |              |  ||  |     +--+ | +--------+|      ||\n' \
         f'++   +---+ +--------+  ||  |     +---++-+   +---+||      ++\n' \
         f'|        | |           ||  +--------+|      |+-+|||       |\n' \
         f'|        | |           |+-----------+|      || ++||       |\n' \
         f'|        | |           +----+ +------+      |+---+|       |\n' \
         f'|        | |                | |             +-----+       |\n' \
         f'|        | |                | |                +-+        |\n' \
         f'|        +-+                +-+                +-+        |\n' \
         f'|                       +------+           +------+       |\n' \
         f'|                       |+----+|           |+----+|       |\n' \
         f'|                       ||+--+||           ||+--+||       |\n' \
         f'|                       |||++|||           |||++|||       |\n' \
         f'+-------------------+   |||++|||      ++   |||++|||      ++\n' \
         f'|                   |   |||+-+||      ||   |||+-+||      ||\n' \
         f'+------+     +------+   ||+---+|      ++   ||+---+|      ++\n' \
         f'|      |     |          |+-++--+           |+-++--+       |\n' \
         f'|      +-+ +-+      +---+--+|          +---+--+|          |\n' \
         f'|        | |        +-------+          +-------+          |\n' \
         f'|        | |                                              |\n' \
         f'|        | |                +-+                +-+        |\n' \
         f'|        | |                +-+                +-+        |\n' \
         f'|        | |            +------+                          |\n' \
         f'|        | |            |+----+|                          |\n' \
         f'|      +-+ +-+          ||+--+||                          |\n' \
         f'|      |     |          |||++|||              +----+      |\n' \
         f'+------+     +------+   |||++|||      ++      |+--+|  ++--+\n' \
         f'|                   |   |||+-+||      ||      ||++||  ||  |\n' \
         f'+-------------------+   ||+---+|      ++      ||++||  ++--+\n' \
         f'|                       |+-++--+              |+--+|      |\n' \
         f'|                   +---+--+|                 +----+      |\n' \
         f'|                   +-------+                             |\n' \
         f'|                                                         |\n' \
         f'|        +-+                +-+                +-+        |\n' \
         f'|        | |                | |                +-+        |\n' \
         f'|        | |                | |                           |\n' \
         f'|  +-----+ |                | +-----+                     |\n' \
         f'|  |+-+    |                |    +-+|                     |\n' \
         f'|  || |  +-+                +-+  | ||                     |\n' \
         f'+--+| +--+    +----------+    +--+ |+--+                 ++\n' \
         f'|   |      +--+          +--+      |   |                 ||\n' \
         f'+---+  +---+   +--------+   +---+  +---+                 ++\n' \
         f'|      |       |        |       |                         |\n' \
         f'|      +-+ +---+        +---+ +-+                         |\n' \
         f'|        | |                | |                           |\n' \
         f'|        | |                | |                           |\n' \
         f'|        | |                | |                +-+        |\n' \
         f'+--------+-+----------------+-+----------------+-+--------+'

start = time.time_ns()
figures_ = break_evil_pieces(ex_xxx)
finish = time.time_ns()
print(f'res: ')
for ind, figure_ in enumerate(figures_, 1):
    print(f'{ind}th figure:\n{figure_}')
print(f'time elapsed: {(finish - start) // 10 ** 6} milliseconds')

# print(f'set_: {set(f"abcdeefcbxyz")}')

# s1 = {1, 98}
# s2 = {1, 2, 98}
# print(f'{s1.issubset(s2)}')

# string_ex = f'abcbaa  bntf   '
# print(f'res: {eliminate_right_spaces(string_ex)}')
