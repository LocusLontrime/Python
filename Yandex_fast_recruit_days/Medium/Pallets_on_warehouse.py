# accepted on coderun
import random


def invalid_pallets(pallets):
    # n, pallets = get_pars()
    print(f'pallets: {list(pallets)}')
    # pallets_sorted = [(max(*p), min(*p)) for p in pallets]
    pallets_sorted = sorted(pallets, key=lambda x: x[0], reverse=True)
    print(f'pallets_sorted: {pallets_sorted}')                                                                # 36.6 98
    largest_height_ = 0
    invalid_ones = 0
    ind_ = 0
    while ind_ < len(pallets_sorted):
        temporal_largest_height_ = largest_height_
        if pallets_sorted[ind_][1] >= largest_height_:
            temporal_largest_height_ = max(temporal_largest_height_, pallets_sorted[ind_][1])
            invalid_ones += 1
            print(f'invalid pallet: {pallets_sorted[ind_]}')
        ind_ += 1
        while ind_ < len(pallets_sorted) and pallets_sorted[ind_][0] == pallets_sorted[ind_ - 1][0]:
            if pallets_sorted[ind_][1] >= largest_height_:
                temporal_largest_height_ = max(temporal_largest_height_, pallets_sorted[ind_][1])
                invalid_ones += 1
                print(f'invalid pallet: {pallets_sorted[ind_]}')
            ind_ += 1
        largest_height_ = temporal_largest_height_
        print(f'temporal_largest_height: {temporal_largest_height_}, largest_height_: {largest_height_}')
    print(f'{invalid_ones}')


def get_pars():
    n = int(input())
    pallets = []
    for i in range(n):
        w, h = map(int, input().split())
        pallets.append((max(w, h), min(w, h)))
    return n, pallets


pallets_ = [(random.randint(1, 1_000), random.randint(1, 1_000)) for _ in range(1_000_000)]


invalid_pallets(pallets_)






















































