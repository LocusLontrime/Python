from typing import Optional
import heapq as hq


class Node:
    def __init__(self, val=0, next_node=None):
        self.val = val
        self.next = next_node

    def __lt__(self, other: 'Node'):
        return self.val < other.val

    def __str__(self):
        return str(self.val)

    def __repr__(self):
        return str(self)

    def full_list_str(self):
        def full_list_str_(node_: 'Node'):
            return f'{node_}' + (f'' if node_.next is None else f'->{full_list_str_(node_.next)}')

        return full_list_str_(self)


def merge_k_lists(lists: list[Optional[Node]]) -> Optional[Node]:
    merged_list = None
    right_node_ = None
    priority_queue = [node_ for node_ in lists]  # condition???
    hq.heapify(priority_queue)
    while priority_queue:
        node_ = hq.heappop(priority_queue)
        if node_.next is not None:
            hq.heappush(priority_queue, node_.next)
        if merged_list is None:
            merged_list = node_
        else:
            right_node_.next = node_
        right_node_ = node_
    return merged_list


ll1 = Node(1, Node(2, Node(3)))
ll2 = Node(2, Node(4, Node(7, Node(98))))
ll3 = Node(3, Node(5))

print(f'll1 head: {ll1}')
print(f'll2 head: {ll2}')
print(f'll3 head: {ll3}')

print(f'full list 1: {ll1.full_list_str()}')
print(f'full list 2: {ll2.full_list_str()}')
print(f'full list 3: {ll3.full_list_str()}')

print(f'res: {merge_k_lists([ll1, ll2, ll3]).full_list_str()}')
print(f'res: {merge_k_lists([])}')







