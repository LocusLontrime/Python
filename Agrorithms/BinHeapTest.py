class GridNode:

    def __init__(self, y: int, x: int, f: int):
        self.y, self.x = y, x
        self.f = f

    def __eq__(self, other):
        if type(self) is not type(other):
            return False
        else:
            return (self.y, self.x) == (other.y, other.x)

    # this is needed for using Node objects in priority queue like heapq and so on
    def __lt__(self, other: 'GridNode'):
        # if self.is_greedy:
        #     return (self.h, self.tiebreaker) < (other.h, other.tiebreaker)
        # else:
        return self.f < other.f

    def __hash__(self):
        return hash((self.y, self.x))

    def __str__(self):
        return f'{self.y, self.x}({self.f})'  # [{hash(self)}]

    def __repr__(self):
        return str(self)


class BinHeap:
    """binary heap with indexation based on heapq.py"""

    def __init__(self, arr=None):
        # the heap itself as an array:
        self._heap = [] if arr is None else arr[::]
        # array of elements' indices:
        self._dict = None
        # building indices' dict:
        self._build_indices_dict()
        # transforming the array into a heap:
        self._heapify()

    def _build_indices_dict(self):
        """Builds an auxiliary mapping to store the indices of elements in the heap"""
        self._dict = {el: i for i, el in enumerate(self._heap)}

    def __getitem__(self, index: int):
        """returns heap's element under the index given"""
        return self._heap[index]

    def __contains__(self, item):
        """checks if the item lies in the heap"""
        return item in self._dict.keys()

    def restore_heap_inv(self, neigh: 'GridNode', temp_f: int):
        """restores the heap invariant after the neigh's priority change"""
        if neigh.f > temp_f:
            # new value is greater:
            self._siftup(self.index(neigh))
        elif neigh.f < temp_f:
            # new value is lower:
            self._siftdown(0, self.index(neigh))

    @property
    def heap(self):
        return self._heap

    def show(self):
        """just prints the heap"""
        print(f'heap: {self._heap}')

    def index(self, el):
        """returns the index of the element given"""
        return self._dict[el]

    def remove(self, el):
        """removes the element given from the heap"""
        self._remove_from_heapq(self.index(el))

    def _remove_from_heapq(self, ind: int):
        """inner remove method"""
        self._dict.pop(self._heap[ind])
        self._heap[ind] = self._heap[-1]
        if ind != len(self._dict):
            self._dict[self._heap[ind]] = ind
        self._heap.pop()
        if ind < len(self._heap):
            self._siftup(ind)
            self._siftdown(0, ind)

    # source code from: https://github.com/python/cpython/blob/main/Lib/heapq.py
    def heappush(self, item):
        """Push item onto heap, maintaining the heap invariant."""
        self._heap.append(item)
        self._dict[item] = (l_ := len(self._heap) - 1)
        self._siftdown(0, l_)

    def heappop(self):
        """Pop the smallest item off the heap, maintaining the heap invariant."""
        self._dict.pop(self._heap[0])
        last_elt = self._heap.pop()  # raises appropriate IndexError if heap is empty
        if self._heap:
            return_item = self._heap[0]
            self._heap[0] = last_elt
            self._dict[last_elt] = 0
            self._siftup(0)
            return return_item
        return last_elt

    def _heapify(self):
        """Transform list into a heap, in-place, in O(len(arr)) time."""
        n = len(self._heap)
        # Transform bottom-up.  The largest index there's any point to looking at
        # is the largest with a child index in-range, so must have 2*i + 1 < n,
        # or i < (n-1)/2.  If n is even = 2*j, this is (2*j-1)/2 = j-1/2 so
        # j-1 is the largest, which is n//2 - 1.  If n is odd = 2*j+1, this is
        # (2*j+1-1)/2 = j so j-1 is the largest, and that's again n//2-1.
        for i in reversed(range(n // 2)):
            self._siftup(i)

    def _siftdown(self, start_pos, pos):
        new_item = self._heap[pos]
        # Follow the path to the root, moving parents down until finding a place
        # new_item fits.
        while pos > start_pos:
            parent_pos = (pos - 1) >> 1
            parent = self._heap[parent_pos]
            if new_item < parent:
                self._heap[pos] = parent
                self._dict[parent] = pos
                pos = parent_pos
                continue
            break
        self._heap[pos] = new_item
        self._dict[new_item] = pos

    def _siftup(self, pos):
        end_pos = len(self._heap)
        start_pos = pos
        new_item = self._heap[pos]
        # Bubble up the smaller child until hitting a leaf.
        child_pos = 2 * pos + 1  # leftmost child position
        while child_pos < end_pos:
            # Set child_pos to index of smaller child.
            right_pos = child_pos + 1
            if right_pos < end_pos and not self._heap[child_pos] < self._heap[right_pos]:
                child_pos = right_pos
            # Move the smaller child up
            self._heap[pos] = self._heap[child_pos]
            self._dict[self._heap[pos]] = pos
            pos = child_pos
            child_pos = 2 * pos + 1
        # The leaf at pos is empty now.  Put new_item there, and bubble it up
        # to its final resting place (by sifting its parents down).
        self._heap[pos] = new_item
        self._dict[new_item] = pos
        self._siftdown(start_pos, pos)


nodes = [GridNode(i, i, 10 - i) for i in range(10)]

print(f'{nodes = }')

bh = BinHeap(nodes)
# bh.heappush(GridNode(11, 11, 98989))

print(f'{bh.heap = }')
print(f'{bh._dict}')

nodes[2].f = 98

bh.restore_heap_inv(nodes[2], 8)

bh._heapify()

print(f'{bh.heap = }')
print(f'{bh._dict}')

bh.remove(nodes[1])

print(f'heap popping: ')
for i in range(10 - 1):
    print(f'{bh.heappop()}')

