class Merge:

    recCounter = 0

    @staticmethod
    def merge_sort(nums: list[int]):
        Merge.recCounter = 0
        length = len(nums)
        sorted_array = Merge.recursive_merge_sort(nums, 0, length - 1)
        print(f'Merge sort is finished, {Merge.recCounter} steps done')
        return sorted_array

    @staticmethod
    def recursive_merge_sort(nums: list[int], left_index: int, right_index: int):

        if left_index == right_index:
            return [ nums[ left_index ] ]  # base case of recursion, when the one element in array remained

        pivotIndex = (left_index + right_index) // 2  # calculating a pivot element

        leftArray = Merge.recursive_merge_sort(nums, left_index, pivotIndex)  # recurrent defining of a new left and right arrays
        rightArray = Merge.recursive_merge_sort(nums, pivotIndex + 1, right_index)

        return Merge.merge(leftArray, rightArray)  # merging the two parts in one array

    @staticmethod
    def merge(left_array: list[int], right_array: list[int]):
        leftLength = len(left_array)
        rightLength = len(right_array)

        result = []
        lP, rP = 0, 0  # two pointers strategy

        while lP < leftLength and rP < rightLength:  # while no array is finished

            # the least one is added to the final array
            if left_array[lP] < right_array[rP]:
                result.append(left_array[lP])
                Merge.recCounter += 1
                lP += 1
            else:
                result.append(right_array[rP])
                rP += 1
                Merge.recCounter += 1

        # now we're adding the elements remained in one of arrays to the resulting one

        # the case in which the elements remained in the left array
        for i in range(lP, leftLength):
            result.append(left_array[i])
            Merge.recCounter += 1

        # the case in which the elements remained in the right array
        for i in range(rP, rightLength):
            result.append(right_array[i])
            Merge.recCounter += 1

        return result
