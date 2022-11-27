# iterative bubble sort method:
def bubble_sort(array: list[int]):
    for j in range(len(array) - 1):
        for i in range(j, len(array) - 1):
            if array[i] > array[i + 1]:
                swap(array, i)
                #  --> that is equivalent to:
                # temp = array[i]
                # array[i] = array[i + 1]
                # array[i + 1] = temp


# recursive method of bubble sort:
def recursive_bubble(array: list[int], j=0, i=10):
    if j < len(array) - 2:
        if i == j - 1:
            recursive_bubble(array, j + 1, len(array) - 2)
        else:
            if array[i] > array[i + 1]:
                swap(array, i)
            recursive_bubble(array, j, i - 1)


# auxiliary method for elements swapping:
def swap(array: list[int], i):
    temp = array[i]
    array[i] = array[i + 1]
    array[i + 1] = temp


arr1 = [1, 98, 6, 36, 98989]
bubble_sort(arr1)
print(arr1)


arr2 = [1, 7, 98, 0, 0, 2, 33, 36, 9, 1, 105, 98989]
recursive_bubble(arr2)
print(arr2)


