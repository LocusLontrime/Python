# array with N + 1 elements consists of numbers from the range [1, N] both inclusive, find any repeated num...

# array is MUTABLE for now
# 1. 0(N^2) runtime, O(1) additional memory?
def repeated_brut(arr: list[int]) -> int:
    for j in range(len(arr)):
        for i in range(j + 1, len(arr)):
            if arr[j] == arr[i]:
                return arr[j]


# 2. O(N) runtime, O(N) additional memory?
def repeated_set(arr: list[int]) -> int:
    uniques = set()
    for el in arr:
        if el in uniques:
            return el
        uniques.add(el)


# 3. O(N*log(N)) runtime, O(1) additional memory?
def repeated_sort(arr: list[int]) -> int:
    arr.sort()
    for i in range(len(arr) - 1):
        if arr[i] == arr[i + 1]:
            return arr[i]


# 4. O(N) runtime, O(1) additional memory?
def repeated_chain(arr: list[int]) -> int:
    i = 0
    while arr[i] > 0:
        temp = arr[i]
        # print(f'i: {i}, arr[{i}]: {arr[i]}')
        arr[i] = -1
        i = temp
    return i


# array is IMMUTABLE for now
# 1. O(N*log(N)) runtime, O(1) additional memory?
def repeated_bin(arr: list[int]) -> int:
    lb, rb = 0, len(arr) - 1
    while lb < rb:
        pi = (lb + rb) // 2
        # <= pivot el:
        lowers = sum([1 for _ in arr if _ <= pi])
        # print(f'lb, rb: {lb, rb} --------- pi, lowers: {pi, lowers}')
        # logic:
        if lowers > pi:
            # repeated one lies to the left from pivot el:
            lb, rb = lb, pi
        else:
            # repeated one lies to the right from pivot el:
            lb, rb = pi + 1, rb
    # print(f'lb, rb: {lb, rb}')
    return lb


# 2. O(N) runtime, O(1) additional memory?
def repeated(arr: list[int]) -> int:
    tortoise = arr[0]
    hare = arr[0]
    # print(f'1 phase......................')
    while True:
        hare = arr[arr[hare]]
        tortoise = arr[tortoise]
        # print(f'hare, tortoise: {hare, tortoise}')
        if hare == tortoise:
            break
    # print(f'2 phase......................')
    tortoise = arr[0]
    while hare != tortoise:
        hare = arr[hare]
        tortoise = arr[tortoise]
        # print(f'hare, tortoise: {hare, tortoise}')
    return hare


# nodes: 7 -> 1 -> 3 -> 2 -> 1 -> 3 -> 2 -> 1 ...
arr_ = [7, 3, 1, 2, 5, 7, 5, 1, 1, 6, 1]  # 7, 3, 1, 2, 5, 7, 5, 1, 1, 6, 1
print(f'repeated el hare and tortoise O(1) am: {repeated(arr_)}')
print(f'repeated el brut: {repeated_brut(arr_)}')
print(f'repeated el set: {repeated_set(arr_)}')
print(f'repeated el bin O(1) am: {repeated_bin(arr_)}')
print(f'repeated el sort: {repeated_sort(arr_[:])}')
print(f'repeated el chain O(1) am: {repeated_chain(arr_[:])}')
