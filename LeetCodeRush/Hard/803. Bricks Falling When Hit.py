# accepted on leetcode.com

walk = ((1, 0), (0, -1), (-1, 0), (0, 1))


def hit_bricks(grid: list[list[int]], hits: list[list[int]]) -> list[int]:
    # linear sizes:
    max_j, max_i = len(grid), len(grid[0])
    roof_ind = max_j * max_i
    # what if we apply all hits at first?
    hits_set = set(tuple(hit) for hit in hits)
    new_grid = [[0 if (j, i) in hits_set else grid[j][i] for i in range(max_i)] for j in range(max_j)]
    print_grid(new_grid)
    # now we should create unions using dsu and dfs:
    # 1. in the beginning, we're creating a DSU forest:
    dsu_forest = DSU(roof_ind + 1)  # + 1 for the roof proto-parental node!
    # 2. secondly, linking all the adjacent nodes from new_grid to get unions:
    for j in range(max_j):
        for i in range(max_i):
            if new_grid[j][i]:
                # the top row connected to the roof:
                if j == 0:
                    # adds this node to the roof union:
                    dsu_forest.union(roof_ind, convert_to_1d(j, i, max_i))
                if j > 0:
                    # unites this node and the upper one:
                    if new_grid[j - 1][i]:
                        dsu_forest.union(convert_to_1d(j, i, max_i), convert_to_1d(j - 1, i, max_i))
                if i > 0:
                    # unites this node and the left one:
                    if new_grid[j][i - 1]:
                        dsu_forest.union(convert_to_1d(j, i, max_i), convert_to_1d(j, i - 1, max_i))
    # finally, iterating through the hits' array in reverse:
    prev_roof_size = dsu_forest.roof_size()
    print(f'initial roof size -> {prev_roof_size}')
    print(f'initial dsu tree -> ')
    dsu_forest.print()
    fallen_blocks_sizes = []
    for hit_j, hit_i in hits[::-1]:
        print(f'-> {hit_j, hit_i = }')
        if grid[hit_j][hit_i]:
            # the top row connected to the roof:
            if hit_j == 0:
                dsu_forest.union(roof_ind, convert_to_1d(hit_j, hit_i, max_i))
            # regular processing:
            for adj_j, adj_i in get_adjacent(hit_j, hit_i, max_j, max_i, grid):
                if new_grid[adj_j][adj_i]:
                    dsu_forest.union(convert_to_1d(hit_j, hit_i, max_i), convert_to_1d(adj_j, adj_i, max_i))
            # we add block on the new grid here:
            new_grid[hit_j][hit_i] = 1
        # process fallen blocks:
        dsu_forest.print()
        new_roof_size = dsu_forest.roof_size()
        print(f'{new_roof_size = }')
        fallen_blocks_sizes += [max(0, new_roof_size - prev_roof_size - 1)]
        prev_roof_size = new_roof_size
    # returns array of fallen blocks (need to be reversed)
    return fallen_blocks_sizes[::-1]


def get_adjacent(j: int, i: int, max_j: int, max_i: int, grid: list[list[int]]) -> list[tuple[int, int]]:
    adjacents = []
    for dj, di in walk:
        j_, i_ = j + dj, i + di
        if 0 <= j_ < max_j and 0 <= i_ < max_i:
            adjacents += [(j_, i_)]
    return adjacents


def print_grid(grid: list[list[int]]):
    for row in grid:
        print(f'{row}')


def convert_to_1d(j: int, i: int, max_i: int) -> int:
    return max_i * j + i


class DSU:
    """Disjoint set union structure, useful for searching the connectivity components in a graph or grid"""
    def __init__(self, size: int):
        self.dsu_tree = [_ for _ in range(size)]
        self.sizes = [1 for _ in range(size)]
        self.ccq = size  # not necessary in our case

    def union(self, x: int, y: int):
        """unites two sets represented by x and y elements"""
        # at first finds the real representatives of sets wit x and y respectively:
        x_set_repr = self.find(x)
        y_set_repr = self.find(y)
        # we continue if x and y are not in the same sets:
        if x_set_repr != y_set_repr:
            # if the sizes of sets are different -> we should put smaller sized item
            # under bigger sized item:
            if self.sizes[x_set_repr] < self.sizes[y_set_repr]:
                self.dsu_tree[x_set_repr] = y_set_repr
                # y set is incremented by x set size:
                self.sizes[y_set_repr] += self.sizes[x_set_repr]
            else:
                self.dsu_tree[y_set_repr] = x_set_repr
                # x set is incremented by y set size:
                self.sizes[x_set_repr] += self.sizes[y_set_repr]
            # ccq decrementing:
            self.ccq -= 1
        print(f'x_set_repr, y_set_repr found: {x_set_repr, y_set_repr}, ccq: {self.ccq}')

    def find(self, x: int) -> int:
        """finds the number of the set that contains x element"""
        if self.dsu_tree[x] != x:
            # if x is not the parent of itself -> x is not the representative of its set:
            self.dsu_tree[x] = self.find(self.dsu_tree[x])
            # here we are ascending to the representative of the set and recursively
            # move i-th node directly under the representative of the set...
        return self.dsu_tree[x]

    def change_repr(self, new_repr: int):
        # changes the representative of the union to the new one from it
        # parental links:
        old_repr = self.find(new_repr)
        self.dsu_tree[old_repr] = new_repr
        self.dsu_tree[new_repr] = new_repr
        # sizes:
        self.sizes[old_repr] -= self.sizes[new_repr]
        self.sizes[new_repr] += self.sizes[old_repr]

    def connectivity_components_q(self):
        ...

    def roof_size(self):
        return self.sizes[self.find(len(self.dsu_tree) - 1)] - 1  # -1 for subtracting quasi roof node

    def print(self):
        print(f'dsu_tree: {self.dsu_tree}')
        print(f'sizes: {self.sizes}')
        print(f'ccq: {self.ccq}')


test_ex = [
    [1, 1, 0, 0, 1, 0, 0],
    [1, 1, 1, 0, 1, 1, 0],
    [1, 0, 1, 1, 1, 0, 0],
    [1, 1, 1, 0, 0, 0, 0],
    [1, 1, 0, 1, 1, 1, 1],
    [1, 0, 0, 0, 1, 1, 0],
    [1, 1, 1, 1, 1, 0, 0]
], [[6, 4], [5, 0], [1, 4]]

test_ex_1 = [
    [1, 0, 0, 0],
    [1, 1, 1, 0]
], [[1, 0]]

test_ex_2 = [
    [1, 0, 0, 0],
    [1, 1, 0, 0]
], [[1, 1], [1, 0]]

test_ex_3 = [
    [1],
    [1],
    [1],
    [1],
    [1]
], [[3, 0], [4, 0], [1, 0], [2, 0], [0, 0]]

test_ex_4 = [
    [1, 0, 1],
    [1, 1, 1]
], [[0, 0], [0, 2], [1, 1]]

test_ex_5 = [
    [1, 1, 1],
    [0, 1, 0],
    [0, 0, 0]
], [[0, 2], [2, 0], [0, 1], [1, 2]]

print(f'test res {hit_bricks(*test_ex)}')                                             # 36 366 98 989 98989 LL LL
print(f'test 1 res {hit_bricks(*test_ex_1)}')
print(f'test 2 res {hit_bricks(*test_ex_2)}')
print(f'test 3 res {hit_bricks(*test_ex_3)}')
print(f'test 4 res {hit_bricks(*test_ex_4)}')
print(f'test 5 res {hit_bricks(*test_ex_5)}')

# 0 1 1 1 1 1
# 0 0 0 1 1 1
# 0 0 1 1 1 1
# 0 0 0 0 0 1
# 0 0 0 0 1 1
#       1   1

