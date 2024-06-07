# accepted on codewars.com
def bananas(s: str) -> set[str]:
    all_bananas = set()
    rec_bananas_seeker(-1, 0, len(s), s, "", "banana", all_bananas)

    return all_bananas


def rec_bananas_seeker(i: int, ind: int, n: int, s: str, thing: str, banana: str, all_bananas: set[str]):
    # base case:
    if ind == len(banana):
        all_bananas.add(thing + '-' * (n - i - 1))
        return
    # core:
    for i_ in range(i + 1, n):
        ch_ = s[i_]
        if ch_ == banana[ind]:
            rec_bananas_seeker(i_, ind + 1, n, s, thing + '-' * (i_ - i - 1) + ch_, banana, all_bananas)


ex_s = "bbananana"

great_s = "bababannnanabanabnanbnabanananabaa"

res = bananas(great_s)

for index, row in enumerate(sorted(res, reverse=True), 1):
    print(f'{index} -> {row}')


