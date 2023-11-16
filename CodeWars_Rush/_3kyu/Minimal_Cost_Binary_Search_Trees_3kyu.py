# accepted on codewars.com
import math


class Tree(object):

    def __init__(self, root, left=None, right=None):
        assert root and type(root) == Node
        if left:
            assert type(left) == Tree and left.root < root
        if right:
            assert type(right) == Tree and root < right.root

        self.left: Tree = left
        self.root: Node = root
        self.right: Tree = right

    def is_leaf(self):
        return not (self.left or self.right)

    def __str__(self):

        flag = self.left is None and self.right is None

        if flag:
            left_str = ''
            right_str = ''
        else:
            left_str = '_' if self.left is None else str(self.left)
            right_str = '_' if self.right is None else str(self.right)

        core = str(self.root)

        gap = '' if flag else ' '

        return f'[{left_str}{gap}{core}{gap}{right_str}]'

    def __repr__(self):
        return str(self)

    def __eq__(self, other):

        if self.root != other.root:
            return False

        if (self.left is not None and other.left is None) or (self.left is None and other.left is not None):
            return False

        if (self.right is not None and other.right is None) or (self.right is None and other.right is not None):
            return False

        if self.left != other.left or self.right != other.right:
            return False

        return True

    def __ne__(self, other):

        return not self == other


class Node(object):

    def __init__(self, value, weight=1):
        self.value = value
        self.weight = weight

    def __str__(self):
        return f'{self.value}:{self.weight}'

    def __lt__(self, other):
        return self.value < other.value

    def __gt__(self, other):
        return self.value > other.value

    def __eq__(self, other):
        return self.value == other.value

    def __ne__(self, other):
        return self.value != other.value


def cost(tree: Tree, depth=1):
    """
    Returns the cost of a tree which root is depth deep.
    """
    if tree is None:
        return 0
    return cost(tree.left, depth + 1) + cost(tree.right, depth + 1) + tree.root.weight * depth


def make_min_tree(node_list: list[Node]):
    """
    node_list is a list of Node objects
    Pre-cond: len(node_list > 0) and node_list is sorted in ascending order
    Returns a minimal cost tree of all nodes in node_list.
    """
    # cost[i][j] = Optimal cost of binary search
    # tree that can be formed from keys[i] to keys[j].
    # cost[0][n-1] will store the resultant cost
    n_ = len(node_list)
    costs = [[(0, None) for _ in range(n_ + 1)] for _ in range(n_ + 1)]
    # For a single key, cost is equal to
    # frequency of the key
    for ind in range(n_):
        costs[ind][ind] = node_list[ind].weight, Tree(node_list[ind])
    return optimal_search_tree(node_list, n_, costs)[1]


def optimal_cost_memoized(nodes, i, j, costs):
    # Reuses cost already calculated for the sub-problems.
    # Since we initialized costs-matrix with 0, None and frequency, one-node-tree for a tree of one node,
    # it can be used as a stop-condition for the border case:
    if costs[i][j][0]:
        return costs[i][j]
    # Calculates the sum of freq[i], freq[i+1], ... freq[j]
    f_sum = sum(node.weight for node in nodes[i: j + 1])
    # Initializes the minimum value by Inf:
    min_ = math.inf
    # One by one considers all elements as root and recursively find cost of the BST,
    # then compares the cost with the min and updates min if it is needed:
    for r in range(i, j + 1):
        cl, left_tree = optimal_cost_memoized(nodes, i, r - 1, costs)
        cr, right_tree = optimal_cost_memoized(nodes, r + 1, j, costs)
        c = cl + cr
        c += f_sum
        if c < min_:
            min_ = c
            # rebuilds tree if better is found:
            tree = Tree(nodes[r], left_tree, right_tree)
            # replace cost with the new optimal cost calculated:
            costs[i][j] = c, tree
    # Return minimum value
    return costs[i][j]


# The main function that calculates minimum
# cost of a Binary Search Tree. It mainly
# uses optimal_cost() to find the optimal cost.
def optimal_search_tree(nodes, n, costs):
    # Here array keys[] is assumed to be
    # sorted in increasing order. If keys[]
    # is not sorted, then add code to sort
    # keys, and rearrange freq[] accordingly.
    return optimal_cost_memoized(nodes, 0, n - 1, costs)


if __name__ == '__main__':
    nodes_ = [Node('A', 10), Node('B', 2), Node('C', 4), Node('D', 9), Node('E', 8)]
    optimal_cost_bin_search_tree = make_min_tree(nodes_)
    opt_cost = cost(optimal_cost_bin_search_tree, 1)
    print("Cost of Optimal BST is", opt_cost)
    print(f'optimal_cost_bin_search_tree: ')
    print(f'{optimal_cost_bin_search_tree}')



