# accepted on codewars.com, get it clear!
class Node:
    def __init__(self, name: str, next_=None):
        self.name = name
        self.next = next_

    def print(self):
        node_ = self
        while node_:
            print(f'{node_}->', end='')
            node_ = node_.next

    def __str__(self):
        return f'{self.name}'


def swap_pairs(head):
    if head is None or head.next is None:
        return head

    node_ = head
    new_head = head.next

    while node_ is not None and node_.next is not None:
        temporal = node_.next
        print(f'temporal: {temporal}')
        node_.next = node_.next.next
        print(f'temporal.next before: {temporal.next}')
        temporal.next = node_
        print(f'temporal.next after: {temporal.next}')
        node_ = node_.next
        print(f'node_ after: {node_}')
        if node_ is not None and node_.next is not None:
            print(f'temporal.next.next before: {temporal.next.next}')
            temporal.next.next = node_.next
            print(f'temporal.next.next after: {temporal.next.next}')

    return new_head


node_list = Node('A', Node('B', Node('C', Node('D', Node('E')))))
swap_pairs(node_list).print()




