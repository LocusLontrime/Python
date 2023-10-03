rec_counter: int


def solve_puzzle(board: list[str], pieces: list[list[int]]):  # 36 366 98 989 LL
    # your code goes here. you can do it!
    print(f'len: {len(pieces)}')
    print(f'pieces: {pieces}')
    for row in board:
        print(f'{row}')


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
    def __init__(self, j: int, i: int, col_link: LinkColumn):
        self.j, self.i = j, i
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
        # root link:
        self.root = LinkColumn(-1)
        # initialization:
        self._initialize_cols_links()
        # solutions:
        self.sols = []
        # rows counter:
        self.row_num = 0

    def _initialize_cols_links(self):
        print(f'cols: {self.cols}')
        # creating LinkColumns:
        prev_ = self.root
        for i in range(self.cols):
            current_col_link = LinkColumn(i)
            prev_.R = current_col_link
            current_col_link.L = prev_
            prev_ = current_col_link

    def __str__(self):
        ...

    def append_row(self, row: list[int]) -> None:  # 1, 0, 0, 0, 0, 0, 1, 1, 0, 1, 0, 0, 0, 1
        assert self.cols == len(row), f'LEVI JEAN IS NOT MY LOVER!!!'
        print(f'appending row: {row}')
        # building new row in DancingLinks:
        column_node_: LinkColumn = self.root
        prev_ = None
        for i, val in enumerate(row):
            column_node_ = column_node_.R
            if val:
                curr_link_node = LinkNode(self.row_num, i, column_node_)
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
        # next row step:
        self.row_num += 1

    def knuth_x(self, solution: list) -> None:
        """Knuth's algorithm X based on Dancing Links"""
        global rec_counter
        rec_counter += 1
        node_ = self.root.R
        print(f'cols sizes: ', end=' ')
        while node_:
            print(f'{node_.size}', end=' ')
            node_ = node_.R
        print()
        # check for exact cover:
        if not self.root.R:
            print(f'SOLUTION FOUND!!!')
            self.sols.append(solution)
            return
        best_col = self.choose_best_col()
        if not best_col.size:  # size == 0
            # there are no solutions in this branch
            print(f'NO SOLUTIONS BRANCH REACHED!!!')
            return
        # covering the best column:
        self.cover_col(best_col)
        # iterating through all the column's LinkNodes:
        link_node_ = best_col.D
        while link_node_:
            # preparing the row to be pushed into the stack of the current solution:
            row_to_be_pushed = self.get_row(link_node_)
            # covering all the crossed columns:
            for node_ in (nodes := self.get_row(link_node_, False)):
                self.cover_col(node_.col_link)
            # recursive deepening:
            self.knuth_x(solution + [row_to_be_pushed])
            # uncovering columns (backtracking)
            for node_ in nodes[::-1]:
                self.uncover_col(node_.col_link)
            link_node_ = link_node_.D
        # uncovering the best column (backtracking):
        self.uncover_col(best_col)

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

    def get_top_left(self):
        ...

    def cover_col(self, col: LinkColumn):  # col -> LinkNode or int?..
        # LR-detaching the ColumnLink:
        self.detach_lr(col)
        # detaching crossed rows:
        for link_node_ in self.get_column_nodes(col):
            # UD-detaching (except the column's link_node_):
            for row_node_ in self.get_row(link_node_, False):
                self.detach_ud(row_node_)

    def uncover_col(self, col):
        # LR-attaching the ColumnLink:
        self.attach_lr(col)
        # attaching crossed rows:
        for link_node_ in self.get_column_nodes(col)[::-1]:  # TODO: optimize if it is possible!!!
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
            if (cs := col_.size) < 2:
                return col_
            if cs < best_col_size:
                best_col, best_col_size = col_, cs
            col_ = col_.R
        return best_col


# r = list(range(10))
# r_ = [i for i in range(10)]
# print(f'r: {r}')
# print(f'r_: {r_}')

dlx = DancingLinks(3 + 9)
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
rows = [
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

for row_ in rows:
    dlx.append_row(row_)

# print(f'\n{dlx}')
rec_counter = 0
dlx.knuth_x([])
print(f'solutions: ')
for sol in dlx.sols:
    print(f'{sol}')
print(f'rec_counter: {rec_counter}')

