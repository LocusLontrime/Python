class Node:
    def __init__(self, val, next_: 'Node' = None):
        self.val = val
        self.next = next_

    def __str__(self):
        return f'{self.val}'

    def __lt__(self, other):
        return self.val < other.val


class NodeList:
    def __init__(self, root: Node = None):
        self.root = root
        self.tail = None

    def __str__(self):
        node_ = self.root
        string = f''
        while node_.next:
            string += f'{node_}->'
            node_ = node_.next
        return string + f'{node_}'

    def __len__(self) -> int:
        """returns the length of the NodeList"""
        length = 0
        node_ = self.root
        while node_:
            length += 1
            node_ = node_.next
        return length

    def get(self, index: int):
        i = 0
        node_ = self.root
        while node_:
            if i == index:
                return node_.val
            # preparation for the next iteration:
            _node = node_
            node_ = node_.next
            i += 1

    def set(self, index: int, val):
        """searches for the node at the index given and then changes its value to the new val"""
        i = 0
        node_ = self.root
        while node_:
            if i == index:
                node_.val = val
                return
            # preparation for the next iteration:
            _node = node_
            node_ = node_.next
            i += 1

    def add(self, new_val):
        """adds a Node to the right (end of the NodeList)"""
        new_node = Node(new_val)
        if self.root:
            self.tail.next = new_node
        else:
            self.root = new_node
        # updating the tail:
        self.tail = new_node

    def insert(self, index: int, value):
        new_node = Node(value)
        i = 0
        node_ = self.root
        _node = None
        while node_:
            if i == index:
                if _node:
                    _node.next = new_node
                    new_node.next = node_
                else:
                    self.root = new_node
                    new_node.next = node_
                return
            # preparation to the next iteration:
            _node = node_
            node_ = node_.next
            i += 1

    def index(self, value) -> int:
        """returns the index of first occurrence of the value given in the NodeList"""
        i = 0
        node_ = self.root
        while node_:
            if node_.val == value:
                return i
            # preparation for the next iteration:
            _node = node_
            node_ = node_.next
            i += 1

    def remove(self, index: int):
        i = 0
        node_ = self.root
        _node = None
        while node_:
            if i == index:
                if _node:
                    _node.next = node_.next
                else:
                    self.root = node_.next
                return
            # preparation to the next iteration:
            _node = node_
            node_ = node_.next
            i += 1

    def max(self):
        if self.root:
            max_val = self.root.val
            i = 0
            node_ = self.root
            while node_:
                if max_val < node_.val:
                    max_val = node_.val
                # preparation for the next iteration:
                _node = node_
                node_ = node_.next
                i += 1
            return max_val
        else:
            raise ValueError(f'Cannot find maximum of an empty sequence!..')

    def min(self):
        if self.root:
            min_val = self.root.val
            i = 0
            node_ = self.root
            while node_:
                if min_val > node_.val:
                    min_val = node_.val
                # preparation for the next iteration:
                _node = node_
                node_ = node_.next
                i += 1
            return min_val
        else:
            raise ValueError(f'Cannot find minimum of an empty sequence!..')


nl = NodeList()
nl.add('A')
nl.add('B')
nl.add('C')
nl.add('D')
nl.add('E')
nl.add('F')
nl.add('G')

print(f'nl: {nl}')
nl.remove(3)
print(f'nl: {nl}')
nl.remove(0)
print(f'nl: {nl}')
nl.set(2, 'N')
print(f'nl: {nl}')
print(f'get(2): {nl.get(2)}')
print(f'nl: {nl}')
print(f'length: {len(nl)}')
print(f'nl: {nl}')
print(f'index of N: {nl.index("N")}')
print(f'nl: {nl}')
nl.insert(2, 'W')
print(f'nl: {nl}')
print(f'max val: {nl.max()}')
print(f'min val: {nl.min()}')
print(f'nl: {nl}')

