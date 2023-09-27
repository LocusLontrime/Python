from collections import defaultdict as d


def minimize_sorrow(k: int, n: int, m: int, pairs: list[tuple[int, int]]) -> int:
    # main process:
    sorrows = []
    repairing = d(list)
    for day, road in pairs:
        if repairing[road]:
            sorrows.append(day - repairing[road][-1])
        repairing[road].append(day)
    print(f'repairing: {repairing}')
    print(f'sorrows: {sorrows}')
    # if all the roads cannot have been repaired by the Election Day:
    if len(repairing) > m:
        return -1
    # sorting the intervals of sorrow:
    sorrows.sort(reverse=True)
    print(f'sorted sorrows: {sorrows}')
    # evaluate the answer:
    all_sorrow = sum(sorrows)  # sum([x[-1] - x[0] for x in repairing.values() if x])
    negative_sorrow = sum(sorrows[:m - len(repairing) + 1])
    print(f'all_sorrow, negative_sorrow: {all_sorrow, negative_sorrow}')
    return all_sorrow - negative_sorrow


pairs_ = [(1, 1), (2, 2), (2, 3), (3, 2), (3, 4), (3, 1), (4, 3), (4, 4), (5, 1), (5, 5)]
k_, n_, m_ = 5, 10, 7

print(f'sorrow: {minimize_sorrow(k_, n_, m_, pairs_)}')




