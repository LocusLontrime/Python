def solve_puzzle(board: list[str], pieces: list[list[int]]):  # 36 366 98 989 LL
    # your code goes here. you can do it!
    print(f'len: {len(pieces)}')
    print(f'pieces: {pieces}')
    for row in board:
        print(f'{row}')


class DancingLinks:
    def __init__(self, cols: int):
        # columns number:
        self.cols = cols
        # header link:
        self.header = LinkColumn(-1)
        # initialization:
        self._initialize_cols_links()
        # solutions:
        self.sols = []
        # rows counter:
        self.row_num = 0

    def _initialize_cols_links(self):
        print(f'cols: {self.cols}')
        # creating LinkColumns:
        prev_ = self.header
        for i in range(self.cols):
            current_col_link = LinkColumn(i)
            prev_.R = current_col_link
            current_col_link.L = prev_
            prev_ = current_col_link

    def __str__(self):
        res = 'DLX----->>>>>\n'
        res += f'down for cols: '
        node_ = self.header
        while node_:
            node__ = node_.head
            while node__:
                res += f'{node__} '
                node__ = node__.D
            res += f'\n'
            node_ = node_.R
        res += f'right for rows:\n'
        node_ = self.header.R.head
        while node_:
            node__ = node_
            while node__:
                res += f'{node__} '
                node__ = node__.R
            # res += f'{node_.R}'
            res += f'\n'
            node_ = node_.D
        return res

    def append_row(self, row: list[int]):  # 1, 0, 0, 0, 0, 0, 1, 1, 0, 1, 0, 0, 0, 1
        assert self.cols == len(row), f'LEVI JEAN IS NOT MY LOVER!!!'
        print(f'appending row: {row}')
        # building new row in DancingLinks:
        column_node_: LinkColumn = self.header
        prev_ = None
        for i, val in enumerate(row):
            column_node_ = column_node_.R
            if val:
                curr_link_node = LinkNode(self.row_num, i)
                if not column_node_.tail:
                    # head'n'tail creation:
                    column_node_.head = column_node_.tail = curr_link_node
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
        # next row step:
        self.row_num += 1

    def cover(self):
        ...

    def uncover(self):
        ...

    def choose_best_col(self):
        ...


class LinkColumn:
    def __init__(self, id_: int):
        self.id = id_  # ???

        self.L = None
        self.R = None

        self.head = None  # ???
        self.tail = None  # ???

        self.size = 0

    def __str__(self):
        return f'{self.id}'


class LinkNode:
    def __init__(self, j: int, i: int):
        self.j, self.i = j, i
        # LR-links:
        self.L = None
        self.R = None
        # UD-links:
        self.U = None
        self.D = None
        # aux pars:
        ...

    def copy(self) -> 'LinkNode':
        copied_node = LinkNode(self.j, self.i)
        copied_node.L = self.L
        copied_node.R = self.R
        copied_node.U = self.U
        copied_node.D = self.D
        return copied_node

    def __str__(self) -> str:
        return f'{self.j, self.i}'


# r = list(range(10))
# r_ = [i for i in range(10)]
# print(f'r: {r}')
# print(f'r_: {r_}')

dlx = DancingLinks(7)
dlx.append_row([1, 0, 0, 0, 1, 0, 1])
dlx.append_row([1, 0, 1, 0, 0, 1, 0])
dlx.append_row([1, 0, 0, 0, 1, 0, 0])
dlx.append_row([1, 1, 0, 1, 1, 0, 1])
dlx.append_row([1, 1, 1, 1, 1, 1, 1])
dlx.append_row([1, 0, 0, 0, 0, 0, 0])
dlx.append_row([1, 0, 0, 1, 0, 1, 1])
dlx.append_row([1, 1, 1, 1, 1, 1, 1])
dlx.append_row([1, 0, 1, 0, 0, 1, 0])
dlx.append_row([1, 0, 1, 0, 0, 1, 0])
dlx.append_row([1, 0, 0, 1, 0, 0, 1])
print(f'\n{dlx}')





