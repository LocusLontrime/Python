# accepted on codewars.com
# from preloaded import Item
from collections import namedtuple  # 36 366 98 989

Item = namedtuple('Item', 'weight price')


# too slow
def greedy_thief_slow(items: list[Item], n: int) -> list[Item]:
    length = len(items)
    valid_combs = list()

    def recursive_seeker(current_item_comb: list[Item], curr_weight: int, index: int):
        for i in range(index, length):
            if (new_curr_weight := curr_weight + (item := items[i]).weight) <= n:
                valid_combs.append(new_current_item_comb := current_item_comb + [item])
                recursive_seeker(new_current_item_comb, new_curr_weight, i + 1)

    # recursive call:
    recursive_seeker([], 0, 0)
    # sorting:
    valid_combs = sorted(valid_combs, key=lambda x: sum(_.price for _ in x), reverse=True)
    # printing:
    print(f'Valid combinations: ')
    for ind, comb in enumerate(valid_combs):
        print(f'{ind + 1}. {comb}, weight: {sum(_.weight for _ in comb)}, price: {sum(_.price for _ in comb)}')
    # returning the best option:
    return valid_combs[0]


# dynamic programming, fast enough:
def greedy_thief(items: list[Item], n: int) -> list[Item]:
    memo = dict()
    best_options = []
    length = len(items)

    def rec_seeker(i_: int, c_: int):
        # base cases:
        if i_ == -1 or c_ == -1:
            return 0
        # body of rec and recurrent relation:
        if (i_, c_) not in memo.keys():
            memo[(i_, c_)] = rec_seeker(i_ - 1, c_) if items[i_].weight > c_ else max(rec_seeker(i_ - 1, c_), rec_seeker(i_ - 1, c_ - items[i_].weight) + items[i_].price)
        return memo[(i_, c_)]

    def rec_restorer(i_, c_):
        if i_ == 0:
            if c_ - items[i_].weight >= 0:
                best_options.append(items[i_])
        if i_ > 0 and c_ >= 0:
            if memo[(i_, c_)] > memo[i_ - 1, c_]:
                # print(f'i_, c_: {i_, c_}')
                best_options.append(items[i_])
                rec_restorer(i_ - 1, c_ - items[i_].weight)
            else:
                rec_restorer(i_ - 1, c_)

    res = rec_seeker(length - 1, n)
    print(f'best price: {res}')
    print(f'memo:\n{memo}')
    rec_restorer(length - 1, n)
    return best_options


items_ = greedy_thief(
    [
        Item(weight=2, price=6),
        Item(weight=2, price=3),
        Item(weight=6, price=5),
        Item(weight=5, price=4),
        Item(weight=4, price=6)
    ],
    10
)

print(f'items: {items_}')

items_x = greedy_thief(
    [
        Item(weight=9, price=1),
        Item(weight=9, price=2),
        Item(weight=9, price=3),
        Item(weight=9, price=4),
        Item(weight=9, price=5)
    ],
    10
)

print(f'items: {items_x}')
