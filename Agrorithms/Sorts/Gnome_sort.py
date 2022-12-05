# original Gnome sort
def gnome_sort(arr: list):

    index = 0
    count = 0

    while 0 <= index < len(arr) - 1:
        # print(f'index: {start}')
        count += 1
        if arr[index] <= arr[index + 1]:
            index += 1
        else:
            swap(arr, index)
            if index != 0:
                index -= 1

    print(f'Gnome sort made {count} steps')


# optimized Gnome sort (Levi Gin), forward movement logic changed:
def gnome_sort_levi(arr: list):

    start = 0
    steps = 0
    count = 0

    while 0 <= start < len(arr) - 1:
        # print(f'index: {start}')
        count += 1
        if arr[start] <= arr[start + 1]:
            start = steps
            steps += 1
        else:
            swap(arr, start)
            if start != 0:
                start -= 1

    print(f'Gnome sort Levi made {count} steps')


def swap(arr: list, i: int):
    arr[i], arr[i + 1] = arr[i + 1], arr[i]


array = [10, 7, 33, 575, 3, 2, 1, 0, 0, 2, 95, 244, 21, 24, 64, 53]
array_x = [11, 9, 2, 11, 111, -9, -98, 9, 98, 98, 0, 989, 98989]
gnome_sort(array_x)
print(array_x)
array_x = [11, 9, 2, 11, 111, -9, -98, 9, 98, 98, 0, 989, 98989]
gnome_sort_levi(array_x)
print(array_x)







