class BinHeap:  # approved...

    def __init__(self, arr):
        self._heap = arr
        self._dict = None
        self._build_indices_dict()
        self._heapify()
        print(f'_dict: {self._dict}')

    def _build_indices_dict(self):
        """Builds an auxiliary mapping to store the indices of elements in the heap"""
        self._dict = {el: i for i, el in enumerate(self._heap)}
        print(f'_dict: {self._dict}')

    def get(self, index: int):
        return self._heap[index]

    def index(self, el):
        return self._dict[el]

    def remove(self, el):
        self._remove_from_heapq(self.index(el))

    def _remove_from_heapq(self, ind: int):
        del self._dict[self._heap[ind]]
        el_ = self._heap[ind] = self._heap[-1]
        self._dict[el_] = ind
        self._heap.pop()
        if ind < len(self._heap):
            # as far as it is known, possible to copy the source code from the heapq module... but how to do that?..
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
        last_elt = self._heap.pop()  # raises appropriate IndexError if heap is empty
        print(f'last_elt: {last_elt}')
        # self._dict
        if self._heap:
            return_item = self._heap[0]
            print(f'return_item: {return_item}')
            del self._dict[self._heap[0]]
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
            # Move the smaller child up.
            el_ = self._heap[pos] = self._heap[child_pos]
            self._dict[el_] = pos
            pos = child_pos
            child_pos = 2 * pos + 1
        # The leaf at pos is empty now.  Put new_item there, and bubble it up
        # to its final resting place (by sifting its parents down).
        self._heap[pos] = new_item
        self._dict[new_item] = pos
        self._siftdown(start_pos, pos)


bin_heap = BinHeap([1, 5, 11, 99, 7, 6, 989, 98989, 98])
print(f'bin_heap: {bin_heap._heap}')
bin_heap.heappop()
print(f'bin_heap: {bin_heap._heap}')
print(f'_dict: {bin_heap._dict}')
bin_heap.heappop()
print(f'bin_heap: {bin_heap._heap}')
print(f'_dict: {bin_heap._dict}')
bin_heap.heappop()
print(f'bin_heap: {bin_heap._heap}')
print(f'_dict: {bin_heap._dict}')
bin_heap.heappop()
print(f'bin_heap: {bin_heap._heap}')
print(f'_dict: {bin_heap._dict}')
bin_heap.heappush(999)
print(f'bin_heap: {bin_heap._heap}')
print(f'_dict: {bin_heap._dict}')
bin_heap.remove(999)
print(f'bin_heap: {bin_heap._heap}')
print(f'_dict: {bin_heap._dict}')

