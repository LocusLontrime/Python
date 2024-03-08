class DSU:
    """Disjoint set union structure, useful for searching the connectivity components in a graph"""
    def __init__(self, size: int):
        self.dsu_tree = [_ for _ in range(size)]
        self.sizes = [1 for _ in range(size)]
        self.ccq = size

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

    def connectivity_components_q(self):
        ...

    def print(self):
        print(f'dsu_tree: {self.dsu_tree}')
        print(f'sizes: {self.sizes}')
        print(f'ccq: {self.ccq}')


dsu = DSU(11)

dsu.union(0, 1)
dsu.union(1, 2)
dsu.union(2, 3)
dsu.union(3, 4)

dsu.print()

dsu.union(5, 7)
dsu.union(7, 6)

dsu.union(8, 9)

dsu.union(1, 6)
dsu.union(8, 7)
dsu.union(9, 10)

# x_el = 4
# print(f'x_el repr: {dsu.find(x_el)}')

dsu.print()





