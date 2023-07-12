# accepted on coderun


class Node:
    def __init__(self, symbol: str, is_key: bool, weight: int = 1):
        self.symbol = symbol
        self.is_key = is_key
        self.weight = weight
        self.children = {}                                                            # 36.6 98


class Trie:
    def __init__(self):
        self.root = Node(' ', False)
        self.uniques = set()

    def insert(self, word: str) -> int:
        ind_ = 0
        node_ = self.root
        pre_flag = False
        saved_ind = -2
        dw = 1 if word not in self.uniques else 0
        # searching the first absence:
        while ind_ < (wl := len(word)) and (wi := word[ind_]) in node_.children.keys():
            node_ = node_.children[wi]
            print(f'w_: {word[: ind_ + 1]}')
            if not pre_flag and node_.weight == 1 and ind_ < wl:
                print(f'w_: {word[: ind_ + 1]} CAUGHT!!!')
                pre_flag = True
                saved_ind = ind_
            node_.weight += dw
            ind_ += 1
        if ind_ == wl and node_.is_key and pre_flag:
            return saved_ind + 1
        # building the word's remainder:
        while ind_ < len(word):
            wi = word[ind_]
            node_.children[wi] = (n_ := Node('wi', False, 1))
            node_ = n_
            ind_ += 1
        # updating the last symbol (the key)
        node_.is_key = True
        # the word cannot be complemented:
        self.uniques.add(word)
        return ind_

    def search(self, word: str) -> tuple[int, bool] | None:
        ind_ = 0
        node_ = self.root
        # searching the first absence:
        while ind_ < (wl := len(word)) and (wi := word[ind_]) in node_.children.keys():
            node_ = node_.children[wi]
            ind_ += 1
        if ind_ == wl:
            return node_.weight, node_.is_key,
        return None


def key_press_q():
    n, words = get_pars()
    trie = Trie()
    buttons_pressed = 0
    for word_ in words:
        d_ = trie.insert(word_)
        buttons_pressed += d_
        print(f'word_: {word_}, d_: {d_}')
    print(f'buttons_pressed: {buttons_pressed}')


def get_pars():
    n = int(input())
    words = input().split()
    return n, words


key_press_q()
