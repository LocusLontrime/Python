# accepted on codewars.com
import math
from collections import defaultdict as d


class Node:
    def __init__(self, lv: int, rv: int, participants: list[str], parent=None):
        # aux info:
        self.participants = participants
        # key or value (data) of the node:
        self.parent = parent
        self.rv = rv
        self.lv = lv
        # children (leafs):
        self.left_node = None
        self.right_node = None
        # weight (auxiliary par, used for index defining):
        self.weight = 1

    def __str__(self):
        hours, mins = divmod(self.lv, 60)
        names = ' '.join(self.participants)
        dh = '0' * (2 - len(str(hours)))
        dm = '0' * (2 - len(str(mins)))
        return f'{dh}{hours}:{dm}{mins} {self.rv - self.lv} {names}'

    def __repr__(self):
        return str(self)


class BIST:
    """Binary searching tree with indexation"""

    def __init__(self):
        self.root = None

    def insert(self, lv: int, rv: int):
        # root check:
        if self.root is None:
            return self.root, 0, self
        # the main algo:
        node_ = self.root
        while True:
            node_.weight += 1
            if node_.rv <= lv:
                if node_.right_node is None:
                    return node_, 1, self  # means right-adding:
                node_ = node_.right_node
            elif node_.lv >= rv:
                if node_.left_node is None:
                    return node_, -1, self  # means left-adding:
                node_ = node_.left_node
            else:
                # intersection:
                return None

    def balance(self, node_: 'Node'):
        # cycle of rotations:
        # print(f"now the {node_}'s sub tree is being balanced...")
        while True:
            # left and right subtrees' weights comparison:
            left_depth = self.get_quasi_depth(node_.left_node)
            right_depth = self.get_quasi_depth(node_.right_node)                      # 36.6 98
            if left_depth > right_depth + 1:
                # right rotation:
                child = node_.left_node
                parent = node_.parent

                if parent is not None:
                    if parent.right_node == node_:
                        parent.right_node = child
                    elif parent.left_node == node_:
                        parent.left_node = child
                else:
                    self.root = child
                child.parent = parent
                node_.parent = child

                node_.left_node = child.right_node
                if node_.left_node is not None:
                    node_.left_node.parent = node_
                                                                                      # 36.6 98
                child.right_node = node_

                node_.weight = self.weight_recalc(node_)  # 1 + self.get_weight(node_.left_node) + self.get_weight(node_.right_node)
                child.weight = self.weight_recalc(child)  # 1 + self.get_weight(child.left_node) + self.get_weight(child.right_node)

                node_ = child
            elif right_depth > left_depth + 1:
                # left rotation:
                child = node_.right_node
                parent = node_.parent

                if parent is not None:
                    if parent.right_node == node_:
                        parent.right_node = child
                    elif parent.left_node == node_:
                        parent.left_node = child
                else:
                    self.root = child
                child.parent = parent
                node_.parent = child

                node_.right_node = child.left_node
                if node_.right_node is not None:
                    node_.right_node.parent = node_

                child.left_node = node_

                node_.weight = self.weight_recalc(node_)  # 1 + self.get_weight(node_.left_node) + self.get_weight(node_.right_node)
                child.weight = self.weight_recalc(child)  # 1 + self.get_weight(child.left_node) + self.get_weight(child.right_node)

                node_ = child

            if node_.parent is not None:
                node_ = node_.parent
            else:
                break

    def weight_recalc(self, node_: 'Node') -> int:
        return 1 + self.get_weight(node_.left_node) + self.get_weight(node_.right_node)

    @staticmethod
    def get_weight(node_: 'Node'):
        return 0 if node_ is None else node_.weight

    @staticmethod
    def get_quasi_depth(node_: 'Node') -> int:
        if node_ is None:
            return 0

        if node_.weight == 1:
            return 1
        elif node_.weight == 2:
            return 2

        depth = math.log2(node_.weight + 1)
        return int(depth) if depth % 1 == 0.0 else math.ceil(depth)

    def print_ascending(self):
        def print_ascending(node_: Node):
            if node_ is not None:
                print_ascending(node_.left_node)
                print(f'{node_}')
                print_ascending(node_.right_node)
        print_ascending(self.root)


def process_queries():
    n, queries = get_pars()
    meetups = d(dict)
    for query in queries:
        if query[0] == 'APPOINT':
            day, time, duration, k = query[1:4 + 1]
            participants = query[5:5 + int(k)]
            hours, mins = map(int, time.split(':'))
            start = hours * 60 + mins
            end = start + int(duration)
            invalid_participants = []
            postponed_insertions = []
            for participant in participants:
                if participant in meetups[int(day)].keys():
                    if (r := meetups[int(day)][participant].insert(start, end)) is None:
                        invalid_participants.append(participant)
                    else:
                        postponed_insertions.append(r)
                else:
                    meetups[int(day)][participant] = BIST()
                    postponed_insertions.append(meetups[int(day)][participant].insert(start, end))
            if invalid_participants:
                print(f'FAIL')
                res = ' '.join(invalid_participants)
                print(f'{res}')
            else:
                for node_, res, tree in postponed_insertions:
                    if res == -1:
                        node_.left_node = Node(start, end, participants, node_)
                        tree.balance(node_.left_node)
                    elif res == 1:
                        node_.right_node = Node(start, end, participants, node_)
                        tree.balance(node_.right_node)
                    else:
                        tree.root = Node(start, end, participants, None)
                print(f'OK')
        else:
            day, name = query[1:1 + 2]
            if name in meetups[int(day)].keys():
                meetups[int(day)][name].print_ascending()


def get_pars():                                                                       # 36.6 98
    n = int(input())
    queries = [input().split() for _ in range(n)]
    return n, queries


process_queries()

