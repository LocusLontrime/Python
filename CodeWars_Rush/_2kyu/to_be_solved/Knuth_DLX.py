import time

rec_counter: int


def solve_puzzle(board: list[str], pieces: list[list[int]]):  # 36 366 98 989 LL
    global rec_counter
    # your code goes here. you can do it!
    # print(f'len: {len(pieces)}')
    # print(f'pieces: {pieces}')
    # for row in board:
    #     print(f'{row}')
    # reconstructing the board:
    board_nums = []
    short_nums = {}
    long_nums = {}
    short_num = 0
    for j, string in enumerate(board):
        board_nums.append([])
        for i, x in enumerate(string):
            if x == ' ':
                board_nums[j].append(1)
            else:
                board_nums[j].append(0)
                long_num = j * len(board[0]) + i
                short_nums[long_num] = short_num
                long_nums[short_num] = long_num
                short_num += 1
    # print(f'board: ')
    # for row in board_nums:
    #     print(f'{row}')
    # print(f'short_nums: {short_nums}')
    # print(f'long_nums: {long_nums}')
    area = sum([row.count(0) for row in board_nums])
    # print(f'area: {area}')
    shift = len(pieces)
    row_length = shift + area
    # print(f'shift: {shift}')
    # print(f'row_length: {row_length}')
    # precalculating some prefix arrays:
    prefix_sums = [[0 for _ in range(len(board[0]) + 1)] for _ in range(len(board))]
    for j in range(len(board)):
        for i in range(len(board[0])):
            prefix_sums[j][i + 1] = prefix_sums[j][i] + board_nums[j][i]
    # dancing links initializing:
    dlx = DancingLinks(row_length)
    # building rows for every shape (piece):
    piece_number = 0
    placements = {}
    for h, w in pieces:
        rows = construct_rows(board_nums, [h, w], shift, short_nums, prefix_sums)
        rows_q = len(rows)
        # print(f'piece_number: {piece_number}')
        for row in rows:
            dlx.append_row([piece_number] + row, [h, w], 0)
        if h != w:
            rows = construct_rows(board_nums, [w, h], shift, short_nums, prefix_sums)
            rows_q += rows_q
            # print(f'piece_number: {piece_number}')
            for row in rows:
                dlx.append_row([piece_number] + row, [h, w], 1)
        placements[(h, w)] = rows_q
        piece_number += 1
    print(f'placements: {placements}')
    # starting knuth's algorithm x:
    rec_counter = 0
    sol = dlx.knuth_x([], placements)
    sol = [[ln.j, *divmod(long_nums[ln.i - shift], len(board[0])), ln.orientation] for ln in sol]
    sol.sort(key=lambda k: k[0])
    sol = [el[1:] for el in sol]
    # print(f'solutions: ')
    print(f'{sol}')
    print(f'rec_counter: {rec_counter}')
    return sol


def get_indices(j: int, i: int, piece: list[int], i_max: int, shift: int, short_nums: dict[int, int]):
    return [short_nums[i_max * j_ + i_] + shift for i_ in range(i, i + piece[1]) for j_ in range(j, j + piece[0])]


def construct_rows(board: list[list[int]], piece: list[int], shift: int, short_nums: dict[int, int],
                   prefix_sums: list[list[int]]):
    # print(f'piece: {piece}')
    # rows:
    rows = []
    # creating aux matrix:
    for i in range(len(board[0]) + 1 - piece[1]):
        consecutives = 0
        for j in range(len(board)):
            if prefix_sums[j][i + piece[1]] - prefix_sums[j][i] == 0:
                consecutives += 1
            else:
                consecutives = 0
            if consecutives >= piece[0]:
                rows.append(get_indices(j + 1 - piece[0], i, piece, len(board[0]), shift, short_nums))
    # print(f'rows built: ')
    # for row in rows:
    #     print(f'{row}')
    # returning rows built:
    return rows


class LinkColumn:
    def __init__(self, id_: int):
        self.id = id_
        # LR-links:
        self.L = None
        self.R = None
        self.D = None
        # needed only for rows appending:
        self.tail = None
        # the current size of the column (updating):
        self.size = 0

    def __str__(self):
        return f'{self.id}'

    def __repr__(self) -> str:
        return str(self)


class LinkNode:
    def __init__(self, j: int, i: int, piece: list[int], orientation: int, col_link: LinkColumn):
        # in our case: j -> piece's number, i -> shifted position...
        self.j, self.i = j, i
        # piece associated with:
        self.piece = piece
        # piece's orientation: 0 -> angle of rotation = 0, 1 -> angle of rotation = 90 degrees
        self.orientation = orientation
        # link to the corresponding LinkColumn (in order to change the size of it while covering a column)...
        self.col_link = col_link
        # LR-links:
        self.L = None
        self.R = None
        # UD-links:
        self.U = None
        self.D = None
        # aux pars:
        ...

    def __str__(self) -> str:
        return f'{self.j, self.i}'

    def __repr__(self) -> str:
        return str(self)


class DancingLinks:
    def __init__(self, cols: int):
        # columns number:
        self.cols = cols
        self.cols_list = []
        # root link:
        self.root = LinkColumn(-1)
        # initialization:
        self._initialize_cols_links()
        # solutions:
        self.sols = []

    def _initialize_cols_links(self):
        # print(f'cols: {self.cols}')
        # creating LinkColumns:
        prev_ = self.root
        for i in range(self.cols):
            current_col_link = LinkColumn(i)
            prev_.R = current_col_link
            current_col_link.L = prev_
            prev_ = current_col_link
            self.cols_list.append(current_col_link)

    def append_row(self, row: list[int], piece: list[int], piece_or: int) -> None:  # 1, 0, 0, 0, 0, 0, 1, 1, 0, 1, 0, 0, 0, 1
        # print(f'appending row: {row}')
        # building new row in DancingLinks:
        prev_ = None
        for val in row:
            column_node_ = self.cols_list[val]
            curr_link_node = LinkNode(row[0], val, piece, piece_or, column_node_)
            if not column_node_.tail:
                # head'n'tail creation:
                column_node_.D = column_node_.tail = curr_link_node
                curr_link_node.U = column_node_
            else:
                # UD-links:
                column_node_.tail.D = curr_link_node
                curr_link_node.U = column_node_.tail
                column_node_.tail = curr_link_node
            # LR-links:
            if prev_:
                prev_.R = curr_link_node
                curr_link_node.L = prev_
            # previous (left) link_node updating:
            prev_ = curr_link_node
            # size updating:
            column_node_.size += 1

    def knuth_x(self, solution: list, placements: dict[tuple[int, int], int]):
        """Knuth's algorithm X based on Dancing Links"""
        global rec_counter
        rec_counter += 1
        if rec_counter % 10_000 == 0:
            print(f'rec_counter: {rec_counter}')
        # node_ = self.root.R
        # print(f'cols sizes: ', end=' ')
        # while node_:
        #     print(f'{node_.size}', end=' ')
        #     node_ = node_.R
        # print()
        # check for exact cover:
        if not self.root.R:
            # print(f'SOLUTION FOUND!!!')
            self.sols.append(solution)
            return solution
        best_col = self.choose_best_col()
        if not best_col.size:  # size == 0
            # there are no solutions in this branch
            # print(f'NO SOLUTIONS BRANCH REACHED!!!')
            return
        # covering the best column:
        self.cover_col(best_col, placements)
        # iterating through all the column's LinkNodes:
        column_nodes = self.get_column_nodes(best_col)  # [::-1]
        for link_node_ in sorted(column_nodes, key=lambda ln: placements[(p := ln.piece)[0], p[1]]):
            # lambda ln: (-(t := ln.piece)[1] * t[0], -max(t[0], t[1]))
            # preparing the leftmost LinkNode in the row to be pushed into the stack of the current solution:
            leftmost_to_be_pushed = self.get_leftmost(link_node_)
            # covering all the crossed columns:
            for node_ in (nodes := self.get_row(link_node_, False)):
                self.cover_col(node_.col_link, placements)
            # recursive deepening:
            if r := self.knuth_x(solution + [leftmost_to_be_pushed], placements):
                return r
            # uncovering columns (backtracking)
            for node_ in nodes[::-1]:
                self.uncover_col(node_.col_link, placements)
        # uncovering the best column (backtracking):
        self.uncover_col(best_col, placements)

    @staticmethod
    def get_leftmost(link_node_: LinkNode) -> LinkNode:
        ln_ = link_node_
        while ln_.L:
            ln_ = ln_.L
        return ln_.R

    @staticmethod
    def get_row(link_node_: LinkNode, full: bool = True) -> list[LinkNode]:
        """retrieves the full row (if full=True) or full row except the node given (if full=False)
        from the LinkNode given (from leftmost to rightmost)"""
        # TODO: do we need leftmost->rightmost order for correct work?..
        nodes = DancingLinks.get_lefts(link_node_)[::-1]
        if full:
            nodes.append(link_node_)
        return nodes + DancingLinks.get_rights(link_node_)

    @staticmethod
    def get_lefts(link_node_: LinkNode) -> list[LinkNode]:
        nodes = []
        ln_ = link_node_.L
        while ln_:
            nodes.append(ln_)
            ln_ = ln_.L
        return nodes

    @staticmethod
    def get_rights(link_node_: LinkNode) -> list[LinkNode]:
        nodes = []
        ln_ = link_node_.R
        while ln_:
            nodes.append(ln_)
            ln_ = ln_.R
        return nodes

    @staticmethod
    def get_column_nodes(col: LinkColumn) -> list[LinkNode]:
        nodes = []
        link_node_ = col.D
        while link_node_:
            nodes.append(link_node_)
            link_node_ = link_node_.D
        return nodes

    def cover_col(self, col: LinkColumn, placements):  # col -> LinkNode or int?..
        # LR-detaching the ColumnLink:
        self.detach_lr(col)
        # detaching crossed rows:
        for link_node_ in self.get_column_nodes(col):
            h, w = link_node_.piece
            placements[h, w] -= 1
            # UD-detaching (except the column's link_node_):
            for row_node_ in self.get_row(link_node_, False):
                self.detach_ud(row_node_)

    def uncover_col(self, col, placements):
        # LR-attaching the ColumnLink:
        self.attach_lr(col)
        # attaching crossed rows:
        for link_node_ in self.get_column_nodes(col)[::-1]:  # TODO: optimize if it is possible!!!
            h, w = link_node_.piece
            placements[h, w] += 1
            # UD-attaching (except the column's link_node_):
            for row_node_ in self.get_row(link_node_, False):
                self.attach_ud(row_node_)

    # TODO: decrease the number of if-checks or eliminate them!..
    @staticmethod
    def attach_lr(link_node: LinkNode or LinkColumn):
        if link_node.R:
            link_node.R.L = link_node
        if link_node.L:
            link_node.L.R = link_node

    @staticmethod
    def attach_ud(link_node: 'LinkNode'):
        if link_node.U:
            link_node.U.D = link_node
        if link_node.D:
            link_node.D.U = link_node
        # column size updating:
        link_node.col_link.size += 1

    @staticmethod
    def detach_lr(link_node: LinkNode or LinkColumn):
        if link_node.R:
            link_node.R.L = link_node.L
        if link_node.L:
            link_node.L.R = link_node.R

    @staticmethod
    def detach_ud(link_node: 'LinkNode'):
        if link_node.U:
            link_node.U.D = link_node.D
        if link_node.D:
            link_node.D.U = link_node.U
        # column size updating:
        link_node.col_link.size -= 1

    def choose_best_col(self) -> LinkColumn:
        """chooses the shortest column"""
        col_ = self.root.R
        best_col, best_col_size = self.root.R, self.root.R.size
        while col_:
            if (cs := col_.size) < 1:
                return col_
            if cs < best_col_size:
                best_col, best_col_size = col_, cs
            col_ = col_.R
        return best_col


# r = list(range(10))
# r_ = [i for i in range(10)]
# print(f'r: {r}')
# print(f'r_: {r_}')

# dlx = DancingLinks(3 + 9)
# random nums:
# dlx.append_row([1, 0, 0, 0, 1, 0, 1])
# dlx.append_row([1, 0, 1, 0, 0, 1, 0])
# dlx.append_row([1, 0, 0, 0, 1, 0, 0])
# dlx.append_row([1, 1, 0, 1, 1, 0, 1])
# dlx.append_row([1, 1, 1, 1, 1, 1, 1])
# dlx.append_row([1, 0, 0, 0, 0, 0, 0])
# dlx.append_row([1, 0, 0, 1, 0, 1, 1])
# dlx.append_row([1, 1, 1, 1, 1, 1, 1])
# dlx.append_row([1, 0, 1, 0, 0, 1, 0])
# dlx.append_row([1, 0, 1, 0, 0, 1, 0])
# dlx.append_row([1, 0, 0, 1, 0, 0, 1])

# three shapes case:
# board:    shape1:     shape2:     shape3:
#   1 2 3       * *            *           *
#   4 5 6       * *            *           *
#   7 8 9                      *
rows_ = [
    # TODO: how can we obtain them in an appropriate and optimized way?..
    # first shape:
    [1, 0, 0, 1, 1, 0, 1, 1, 0, 0, 0, 0],
    [1, 0, 0, 0, 1, 1, 0, 1, 1, 0, 0, 0],
    [1, 0, 0, 0, 0, 0, 1, 1, 0, 1, 1, 0],
    [1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 1],
    # second one:
    [0, 1, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0],
    [0, 1, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0],
    [0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1],
    [0, 1, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0],
    [0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0],
    [0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1],
    # third one:
    [0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0],
    [0, 0, 1, 0, 0, 0, 1, 1, 0, 0, 0, 0],
    [0, 0, 1, 0, 0, 0, 0, 1, 1, 0, 0, 0],
    [0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 1, 0],
    [0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1],
    [0, 0, 1, 1, 0, 0, 1, 0, 0, 0, 0, 0],
    [0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0],
    [0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0],
    [0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0],
    [0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 1, 0],
    [0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 1]
]  # approx right!!! needs more tests...

# for row_ in rows_:
#     dlx.append_row(row_)
#
# # print(f'\n{dlx}')
# rec_counter = 0
# dlx.knuth_x([])
# print(f'solutions: ')
# for sol in dlx.sols:
#     print(f'{sol}')
# print(f'rec_counter: {rec_counter}')

board_ = [
    '            ',
    ' 00000      ',
    ' 00000      ',
    ' 00000   00 ',
    '       000  ',
    '   00  000  ',
    ' 0000 00    ',
    ' 0000 00    ',
    ' 00   000 0 ',
    '      000 0 ',
    '  0       0 ',
    '000         '
]
pieces_ = [[1, 1], [1, 1], [1, 2], [1, 2], [1, 2], [1, 3], [1, 3], [1, 4], [1, 4], [2, 2], [2, 2], [2, 3], [2, 3],
           [2, 5]]

board_2 = [
    '          ',
    '          ',
    '  00  00  ',
    '  00  00  ',
    '          ',
    ' 0  00  0 ',
    ' 00    00 ',
    '  000000  ',
    '  000000  ',
    '          '
]

pieces_2 = [[1, 1], [1, 1], [1, 2], [1, 2], [1, 2], [1, 2], [1, 3], [1, 3], [1, 4], [2, 2], [2, 2]]

board_3 = [
    "   0000000000   ",
    "      0000      ",
    "      0000      ",
    " 00000000000000 ",
    " 00000000000000 ",
    "      0000      ",
    "      0000      ",
    "      0000      ",
    "      0000      ",
    "      0000      ",
    "      0000      ",
    "     00000      ",
    "    000 00   00 ",
    "  0000  0000000 ",
    " 000    0000000 ",
    "                "
]

pieces_3 = [[1, 1], [1, 1], [1, 1], [1, 1], [1, 2], [1, 2], [1, 2], [1, 2], [1, 3], [1, 3], [1, 3], [1, 3], [1, 4],
            [1, 4], [1, 4], [1, 4], [1, 5], [1, 7], [1, 7], [1, 12], [2, 2], [2, 2], [2, 3], [2, 4], [2, 5]]

board_4 = [
    "  00       0    ",
    "          00    ",
    " 0000      00   ",
    "  0000000   0000",
    " 000   00   0000",
    " 000  0000000000",
    "0000  0 00000000",
    "0   000 0000 000",
    "0 000   0000 000",
    "  000   0000  00",
    "  000  00000   0",
    "  000000        ",
    "     000000     ",
    " 00  00   00    ",
    " 00  00    0    ",
    " 00  00    0    "
]

pieces_4 = [[1, 1], [1, 1], [1, 1], [1, 2], [1, 2], [1, 2], [1, 2], [1, 2], [1, 3], [1, 3], [1, 3], [1, 3], [1, 4],
            [1, 4], [1, 4], [1, 7], [2, 2], [2, 2], [2, 3], [2, 5], [3, 3], [3, 4], [4, 4], [4, 5]]

board_5 = [
    "     0          ",
    "     0      0   ",
    " 00000   0  0   ",
    " 0000     0000  ",
    " 0000000000  0  ",
    " 000000000  00  ",
    " 0000000000000  ",
    " 000000000000   ",
    "  00000000000   ",
    "   0000000   0  ",
    "    0  000   000",
    "           0    ",
    "        00 0    ",
    "     0000000    ",
    " 000000    0 0  ",
    "00           0  "]

pieces_5 = [[1, 1], [1, 1], [1, 1], [1, 1], [1, 1], [1, 1], [1, 2], [1, 2], [1, 2], [1, 2], [1, 2], [1, 3], [1, 3],
            [1, 3], [1, 3], [1, 3], [1, 4], [1, 4], [1, 6], [1, 6], [2, 2], [3, 3], [4, 6], [5, 5]]

board_6 = [
    "00     000     ",
    " 000           ",
    " 000  0  0000  ",
    " 000  00 00000 ",
    " 000  00  0000 ",
    "  00  00     0 ",
    "  00  00  00000",
    "  00000000000  ",
    "   00    0     ",
    "   00  000 00  ",
    "       000  00 ",
    "       000  00 ",
    "        0    0 ",
    "            00 ",
    "            0  "]

pieces_6 = [[1, 1], [1, 1], [1, 2], [1, 2], [1, 2], [1, 2], [1, 2], [1, 3], [1, 3], [1, 3], [1, 3], [1, 3], [1, 4],
            [1, 4], [1, 5], [1, 8], [2, 2], [2, 2], [2, 4], [3, 3], [3, 4]]

board_7 = [
    "              ",
    "          000 ",
    "  00 00000000 ",
    "   0000 00000 ",
    "    00  00000 ",
    "    00     0  ",
    "  0 000000 0  ",
    " 00000   000  ",
    " 00000   00   ",
    "     0        ",
    "   00000000   ",
    "   00000000   ",
    "   00000000   ",
    "              "]

pieces_7 = [[1, 1], [1, 1], [1, 2], [1, 2], [1, 2], [1, 2], [1, 3], [1, 3], [1, 4], [1, 5], [1, 6], [2, 2], [2, 2],
            [2, 4], [3, 4], [3, 7]]

board_8 = [
    "             ",
    "             ",
    " 0000    00  ",
    "000000  0000 ",
    "00     00  00",
    "00     00  00",
    "00 000 00  00",
    "00 000 00  00",
    "00  00 00  00",
    "000000  0000 ",
    " 0000    00  ",
    "             ",
    "             "
]

pieces_8 = [[1, 1], [1, 1], [1, 1], [1, 1], [1, 1], [1, 2], [1, 2], [1, 2], [1, 2], [1, 2], [1, 3], [1, 3], [1, 3],
            [1, 3], [1, 4], [1, 4], [1, 4], [1, 4], [1, 5], [2, 2], [2, 4], [2, 5]]

board_9 = [
    "            ",
    " 0 0     0  ",
    "00000   00  ",
    " 0 0  0000  ",
    "00000   00  ",
    " 0 0    00  ",
    "        00  ",
    "        00  ",
    "        00  ",
    "        00  ",
    "      000000",
    "            "
]

pieces_9 = [[1, 1], [1, 1], [1, 1], [1, 1], [1, 1], [1, 2], [1, 2], [1, 2], [1, 3], [1, 3], [1, 3], [1, 3], [1, 4],
            [2, 2], [2, 5]]

board_10 = [
    "                    ",
    "        0000        ",
    "       000000       ",
    "      00000000      ",
    "      00000000      ",
    "      00000000      ",
    "      00000000      ",
    "      00 00 00      ",
    "     0000000000     ",
    "    000000000000    ",
    "   00000000000000   ",
    "  0000000000000000  ",
    "  0000000000000000  ",
    " 00  0        0  00 ",
    " 0   0        0   0 ",
    " 0   0        0   0 ",
    "        0  0        ",
    "        0000        ",
    "         00         ",
    "                    "
]

pieces_10 = [[1, 1], [1, 1], [1, 1], [1, 1], [1, 1], [1, 1], [1, 1], [1, 2], [1, 2], [1, 2], [1, 2], [1, 2], [1, 2],
             [1, 2], [1, 2], [1, 3], [1, 3], [1, 3], [1, 3], [1, 3], [1, 4], [1, 5], [1, 6], [1, 7], [1, 7], [1, 8],
             [2, 2], [2, 2], [2, 2], [2, 3], [2, 3], [2, 7], [2, 8], [3, 3]]

board_11 = [
    "00       00         ",
    "00       00         ",
    "00       00    0000 ",
    "0000     000000000  ",
    "0000000000 00  000  ",
    "00         00  000  ",
    "00         00  000  ",
    " 000000000000     0 ",
    "  0000  0   0000  0 ",
    "    000000000000  0 ",
    "    000000000000 000",
    "  0000 000000000 0  ",
    "  000000 0000000 0  ",
    "      0000       0  ",
    "                 0  ",
    "               000  ",
    "  0            00   ",
    " 000      000000    ",
    " 00       00        ",
    "   00   00000       "
]

pieces_11 = [[1, 1], [1, 1], [1, 1], [1, 1], [1, 1], [1, 2], [1, 2], [1, 2], [1, 2], [1, 2], [1, 3], [1, 3], [1, 3],
             [1, 4], [1, 4], [1, 4], [1, 4], [1, 6], [1, 12], [2, 2], [2, 2], [2, 2], [2, 2], [2, 3], [2, 3], [2, 4],
             [2, 4], [2, 5], [2, 7], [3, 5], [4, 7]]

start = time.time_ns()
# solve_puzzle(board_, pieces_)
# solve_puzzle(board_2, pieces_2)
# solve_puzzle(board_3, pieces_3)
# solve_puzzle(board_4, pieces_4)
# solve_puzzle(board_5, pieces_5)
# solve_puzzle(board_6, pieces_6)
# solve_puzzle(board_7, pieces_7)
# solve_puzzle(board_8, pieces_8)
# solve_puzzle(board_9, pieces_9)
# solve_puzzle(board_10, pieces_10)
solve_puzzle(board_11, pieces_11)
finish = time.time_ns()
print(f'time elapsed str: {(finish - start) // 10 ** 6} milliseconds')

