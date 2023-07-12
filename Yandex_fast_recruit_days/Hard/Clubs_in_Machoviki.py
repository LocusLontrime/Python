# accepted on coderun
import sys
import heapq


class MaxHeap:

    # Initialize the max heap
    def __init__(self, data=None):
        if data is None:
            self.data = []
        else:
            self.data = [-i for i in data]
            heapq.heapify(self.data)

    # Push item onto max heap, maintaining the heap invariant
    def push(self, item):
        heapq.heappush(self.data, -item)

    # Pop the largest item off the max heap, maintaining the heap invariant
    def pop(self):
        return -heapq.heappop(self.data)

    # Pop and return the current largest value, and add the new item
    def replace(self, item):
        return heapq.heapreplace(self.data, -item)

    # Return the current largest value in the max heap
    def top(self):
        return -self.data[0]


def best_sequence():
    n = get_pars()
    graph = [[] for _ in range(n + 1)]
    degrees = {_: 0 for _ in range(n + 1)}
    sequence = []
    max_heap = MaxHeap()
    # building a graph:
    for j in range(1, n + 1):
        nums = list(map(int, input().split()))
        length = nums[0]
        for i in range(0, length):
            graph[j].append(vertex_ := nums[i + 1])
            degrees[vertex_] += 1
    # shaping a max_heap:
    for i in range(1, n + 1):
        if degrees[i] == 0:
            max_heap.push(i)
    # max topological sort:
    while max_heap.data:
        vertex_ = max_heap.pop()
        sequence.append(str(vertex_))
        # removing the edges of a kind (vertex_, ...) from graph:
        for i in range(len(graph[vertex_])):
            to_vertex_ = graph[vertex_][i]
            degrees[to_vertex_] -= 1
            if degrees[to_vertex_] == 0:
                max_heap.push(to_vertex_)
    print(f'{" ".join(sequence[::-1])}')


def get_pars() -> int:
    return int(input())



