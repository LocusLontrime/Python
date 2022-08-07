# accepted on codewars.com
def pick_peaks(arr):
    # two pointers approach
    left_pointer = 0
    right_pointer = 0

    positions = []
    maximums = []

    while right_pointer < len(arr) - 1:
        if arr[right_pointer + 1] == arr[right_pointer]:
            right_pointer += 1
        else:
            if (arr[left_pointer - 1] - arr[left_pointer] < 0) and (arr[right_pointer + 1] - arr[left_pointer] < 0) and left_pointer != 0:
                positions.append(left_pointer)
                maximums.append((arr[left_pointer]))
            right_pointer += 1
            left_pointer = right_pointer

    return {'pos': positions, 'peaks': maximums}


print(pick_peaks([3,2,3,6,4,1,2,3,2,1,2,3]))
print(pick_peaks([1,2,5,4,3,2,3,6,4,1,2,3,3,4,5,3,2,1,2,3,5,5,4,3]))
