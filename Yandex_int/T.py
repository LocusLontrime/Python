def find_target(arr: list[int], x: int) -> tuple[int, int] or None:
    prefix_sums = [0] * (length := len(arr) + 1)
    print(f'prefix_sums: {prefix_sums}')
    d = {0: 0}
    for i in range(length - 1):
        prefix_sums[i + 1] = prefix_sums[i] + arr[i]
        print(f'prefix_sums: {prefix_sums}')
        if prefix_sums[i + 1] - x in d.keys():
            return d[prefix_sums[i + 1] - x], i
        d[prefix_sums[i + 1]] = i + 1
    return None


arr_ = [9, -6, 5, 1, 4, -2]  # [0, 9, 3, 8, 9, 13, 11]
print(f'res: {find_target(arr_, 10)}')


