# accepted on codewars.com
import random
import time

walk = tuple((j, i) for j in range(-1, 2) for i in range(-1, 2) if j or i)


# counts rec calls, but decreases performance...
rec_counter: int


class Node:
    def __init__(self, symbol: str, is_key: bool):
        self.symbol = symbol
        self.is_key = is_key
        self.children = {}                                                            # 36.6 98


class Trie:
    def __init__(self):
        self.root = Node(' ', False)

    def insert(self, word_: str):
        ind_ = 0
        node_ = self.root
        # searching the first absence:
        while ind_ < len(word_) and (wi := word_[ind_]) in node_.children.keys():
            node_ = node_.children[wi]
            # print(f'w_: {word[: ind_ + 1]}')
            ind_ += 1
        # building the word's remainder:
        while ind_ < len(word_):
            wi = word_[ind_]
            node_.children[wi] = (n_ := Node(wi, False))
            node_ = n_
            ind_ += 1
        # updating the last symbol (the key)
        node_.is_key = True


words_trie = Trie()


words_ = ""
with open("C:\\Users\\langr\\PycharmProjects\\AmberCode\\CodeWars_Rush\\_4kyu\\WORDS_.txt") as f:
    for line in f:
        words_ = line.split()
        # print(f'{words_ = }')


for word in words_:
    words_trie.insert(word)


def squaredle(puzzle: str):
    global rec_counter
    rec_counter = 0

    grid = [row for row in puzzle.split('-')]
    print(f'Grid: ')
    print(f'{"_" * (len(grid[0]) + 2)}')
    for row in grid:
        print(f'|{row}|')
    print(f'{"-" * (len(grid[0]) + 2)}')

    # visited 2D-array building:
    visited = [[False for _ in range(len(grid[0]))] for _ in range(len(grid))]

    # cycling all over the starting points:
    words_found = set()
    for j in range(max_j := len(grid)):
        for i in range(max_i := len(grid[0])):
            rec_seeker(j, i, max_j, max_i, grid, words_trie.root, '', words_found, visited)

    # words' sorting:
    words_found = list(words_found)
    words_found.sort(key=lambda x: (len(x), x))
    return words_found


def rec_seeker(j: int, i: int, max_j: int, max_i: int, grid: list[str], trie_node_: Node, word_: str, words_found: set[str], visited: list[list[bool]]):
    global rec_counter
    rec_counter += 1
    # print(f'{j, i} -> {word_ = }')
    # border case:
    if trie_node_.is_key:
        words_found.add(word_)
    # body of rec:
    if 0 <= j < max_j and 0 <= i < max_i:
        if not visited[j][i] and (gji := grid[j][i]) in trie_node_.children.keys():
            # visiting a point:
            visited[j][i] = True
            # current node:
            node_ = trie_node_.children[gji]
            # getting neighs:
            for dj, di in walk:
                # recurrent call:
                rec_seeker(j + dj, i + di, max_j, max_i, grid, node_, word_ + gji, words_found, visited)  #
            # unvisiting point:
            visited[j][i] = False


# print(f'res: {words_trie.search("calorie")}')                                       #
# print(f'res: {words_trie.search("zzz")}')
# print(f'res: {words_trie.search("calori")}')                                        #

sq_1 = 'qgru-ntbo-oiel-tohs'
sq_2 = 'ka-ta'
sq_3 = 'plz-euz'
sq_x = 'is k e eyn-gkes  pv n-pxivkyroh -qzanhkjj b- lgel u u - mpylvhwko-izhggijlre-untxwl kje-w klx oe o-lcp brsrw '
size = 100
sq_z = '-'.join([''.join([chr(random.randint(97, 122)) for i in range(size)]) for j in range(size)])  #

start = time.time_ns()
wf = squaredle(sq_z)
finish = time.time_ns()
print(f'time elapsed: {(finish - start) // 10 ** 6} milliseconds')
print(f'Words found: {wf}')
print(f'Words found size: {len(wf)}')
print(f'{rec_counter = }')
