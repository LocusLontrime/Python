def get_slice(arr: list[int], indices: str) -> list[int]:
    def translate(index: int) -> int:
        return index if index >= 0 else n + index

    indices_ = indices.split(':')
    print(f'{indices_ = }')
    indices_parsed = [int(el) for el in indices_ if el]
    print(f'{indices_parsed = }')

    n = len(arr)
    delta = 1
    li, ri = 0, n

    if indices[0] == ':':
        ri = translate(indices_parsed[0])
    else:
        li = translate(indices_parsed[0])
        if len(indices_parsed) != 1:
            ri = translate(indices_parsed[1])
            if len(indices_parsed) == 3:
                delta = translate(indices_parsed[2])

    return [arr[i] for i in range(li, ri, delta)]


array = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]

print(f'{get_slice(array, f"4:9:2")}')
print(f'{get_slice(array, f"4:9")}')
print(f'{get_slice(array, f":9")}')
print(f'{get_slice(array, f"9:")}')
print(f'{get_slice(array, f"-2:")}')
print(f'{get_slice(array, f":-2")}')
