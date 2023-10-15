# accepted on codewars.com
import heapq
from collections import deque


# takes: str; returns: [ (str, int) ] (Strings in return value are single characters)
# makes a list of tuples[char, freq] for a base string to be encoded
def frequencies(s) -> list[tuple[str, int]]:

    # constructing a frequency dictionary:
    freq_dict = dict()
    for ch in s:
        if ch in freq_dict.keys():
            freq_dict[ch] += 1
        else:
            freq_dict[ch] = 1

    # dict to --> list of tuples:
    freq_list = list(freq_dict.items())

    # sort a list of tuples by freq:
    return list(sorted(freq_list, key=lambda x: -x[1]))


def get_huffman_tree(freqs):
    # transform list of tuples to list of nodes
    nodes = list()
    for tup in freqs:
        nodes.append(Node(tup[0], tup[1]))

    # constructing deque of nodes:
    heapq.heapify(nodes)

    # building the Huffman Tree:
    while len(nodes) > 1:
        rightmost_node = heapq.heappop(nodes)
        leftmost_node = heapq.heappop(nodes)

        new_node = Node('', rightmost_node.freq + leftmost_node.freq, leftmost_node, rightmost_node)
        heapq.heappush(nodes, new_node)

    # the one in deque is root:
    root = heapq.heappop(nodes)

    return root


def get_huffman_dict(freqs):
    root = get_huffman_tree(freqs)

    # auxiliary recursive method for compiling a encoding dictionary:
    def req_seeker(node, representation, new_repr_dict) -> None:
        if node.is_leaf():
            new_repr_dict[node.char] = representation
        else:
            req_seeker(node.left_leaf, representation + '0', new_repr_dict)
            req_seeker(node.right_leaf, representation + '1', new_repr_dict)

    huffman_dict = dict()
    # rec call:
    req_seeker(root, '', huffman_dict)

    print(f'huffman_dict: {huffman_dict}')
    return huffman_dict


# takes: [ (str, int) ], str; returns: String (with "0" and "1")
def encode(freqs, s):
    # border case:
    if len(freqs) < 2:
        return None

    huffman_dict = get_huffman_dict(freqs)

    # encoding itself:
    ans = ''
    for ch in s:
        ans += huffman_dict[ch]

    return ans


# takes [ [str, int] ], str (with "0" and "1"); returns: str
def decode(freqs, bits):

    # border case:
    if len(freqs) < 2:
        return None

    root = get_huffman_tree(freqs)

    def rec_seeker(node, bits_index):

        if node.is_leaf():
            return node.char, bits_index

        curr_bit = bits[bits_index]

        if curr_bit == '0':
            return rec_seeker(node.left_leaf, bits_index + 1)
        else:
            return rec_seeker(node.right_leaf, bits_index + 1)

    # decoding itself:
    index = 0
    ans = ''
    while index < len(bits):
        char, index = rec_seeker(root, index)
        ans += char
        print(f'char: {char}, index: {index}')

    return ans


# class of a node for our encoding tree
class Node:
    def __init__(self, char, freq, left_node=None, right_node=None):
        self.char = char
        self.freq = freq
        self.left_leaf = left_node
        self.right_leaf = right_node

    # this is needed for using Node objects in priority queue like heapq and so on
    def __lt__(self, other):
        return self.freq < other.freq

    def add_l_node(self, sub_l_node):
        if sub_l_node is not None:
            self.left_leaf = sub_l_node

    def add_r_node(self, sub_r_node):
        if sub_r_node is not None:
            self.right_leaf = sub_r_node

    # checks if the node is leaf (it means if this node has no sub-nodes)
    def is_leaf(self):
        return self.left_leaf is None and self.right_leaf is None


# some testing
# print(f := frequencies(string := "Levi Gin is not a lover."))
# print(e := encode(f, string))
#
# print(f'e: {e}')
#
# print(decode(f, e))

print(frequencies('aaaabcc'))
