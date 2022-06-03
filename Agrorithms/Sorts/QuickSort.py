class Quick:

    recCounter = 0

    @staticmethod
    def quick_sort(array: list[int]) -> None:
        Quick.recCounter = 0
        length = len(array)
        Quick.recursive_quick_sort(array, 0, length - 1)
        print(f'Quick sort is finished, {Quick.recCounter} steps done')

    @staticmethod
    def recursive_quick_sort(array: list[int], left_border: int, right_border: int) -> None:
        # border case of list of 1 element
        if left_border == right_border:
            return

        pivotElement = (array[left_border] + array[right_border]) // 2  # at first, we define the pivotElement(median)

        # Hoare's Partition
        pivotIndex = Quick.hoare_partition(array, left_border, right_border, pivotElement)  # here we're finding the pivotIndex

        Quick.recursive_quick_sort(array, left_border, pivotIndex)  # recursive tree building, divide and conquer tactics
        Quick.recursive_quick_sort(array, pivotIndex + 1, right_border)

    @staticmethod
    def hoare_partition(array: list[int], left_border: int, right_border: int, pivot_element: int) -> int:  # Hoare's partition part, aux to main method

        while True:

            while array[left_border] < pivot_element:  # skipping the elements that stayed at their place on the left side
                left_border += 1
                Quick.recCounter += 1

            while array[right_border] > pivot_element:  # skipping the elements that stayed at their place on the right side
                right_border -= 1
                Quick.recCounter += 1

            if left_border < right_border:  # we are swapping two elements if they are both stay at wrong places
                Quick.ints_permutation(array, left_border, right_border)
                left_border += 1
                right_border -= 1
            else:
                return right_border

    @staticmethod
    def ints_permutation(array: list[int],  i: int, j: int) -> None:  # swapping two array's elements
        temp = array[i]
        array[i] = array[j]
        array[j] = temp
        Quick.recCounter += 1

