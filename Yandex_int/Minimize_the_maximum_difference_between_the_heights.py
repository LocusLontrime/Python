def min_max(towers: list[int], k: int) -> int:
    if len(towers) < 2:
        return -1
    sorted_towers = sorted(towers)
    n = len(sorted_towers)
    min_h, max_h = sorted_towers[0], sorted_towers[-1]
    ans = max_h - min_h
    for i in range(0, n - 1):  # or n?
        min_h = min(sorted_towers[0], sorted_towers[i + 1] - k)
        max_h = max(sorted_towers[-1], sorted_towers[i] + k)
        ans = min(ans, max_h - min_h)
    # returns res:
    return ans


arr_ = []
arr_x = [1]
arr = [7, 4, 8, 8, 8, 9]
k_ = 6
print(f'res: {min_max(arr, k_)}')
print(f'res: {min_max(arr_x, k_)}')
print(f'res: {min_max(arr_, k_)}')

print(f'{arr[-1]}')

