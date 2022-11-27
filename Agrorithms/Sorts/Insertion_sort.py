def insertion_sort(array: list[int]):
    steps_counter = 0

    for i in range(1, len(array)):
        current_value = array[i]
        j = i - 1

        # gets the element at each iteration and locates it into the sorted part of array
        while j >= 0 and array[j] > current_value:

            array[j + 1] = array[j]
            j -= 1
            steps_counter += 1

        array[j + 1] = current_value


arr = [111, 5, 1, 15, 98, 9898, 1, 98989]
insertion_sort(arr)
print(arr)

