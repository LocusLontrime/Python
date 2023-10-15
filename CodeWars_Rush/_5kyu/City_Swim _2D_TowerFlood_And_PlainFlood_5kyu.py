# accepted on codewars.com
def rain_volume(histogram: list[int]) -> int:
    if not histogram:
        return 0
    li, ri = 0, len(histogram) - 1
    lmh, rmh = histogram[li], histogram[ri]
    water_drops = 0
    while ri >= li:
        if lmh < rmh:
            delta = lmh - histogram[li]
            lmh = max(lmh, histogram[li])
            li += 1
        else:
            delta = rmh - histogram[ri]
            rmh = max(rmh, histogram[ri])
            ri -= 1
        water_drops += (delta if delta > 0 else 0)
    return water_drops


arr = [15, 0, 6, 10, 11, 2, 5]  # 20
arr_ = [1, 0, 5, 2, 6, 3, 10]
print(f'water drops: {rain_volume(arr_)}')


