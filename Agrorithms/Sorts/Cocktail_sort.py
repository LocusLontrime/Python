# Levi Gin
def cocktail_sort(arr: list):
    start = 0
    end = len(arr) - 1

    while start < end:

        for i in range(start, end):
            if arr[i] > arr[i + 1]:
                swap(arr, i)
        start += 1

        for i in range(end, start - 1, -1):
            if arr[i] < arr[i - 1]:
                swap(arr, i - 1)
        end -= 1


def swap(arr: list, i: int):
    arr[i], arr[i + 1] = arr[i + 1], arr[i]


array = [10, 7, 33, 575, 3, 2, 1, 0, 0, 2, 95, 244, 21, 24, 64, 53]
cocktail_sort(array)
print(array)


