def consecutive(arr, a, b):  # accepted on codewars
    # Do some magic
    for i in range(0, len(arr) - 1):
        if arr[i] == a and arr[i + 1] == b:
            return True
        elif arr[i] == b and arr[i + 1] == a:
            return True
    return False


print(consecutive([1, 3, 5, 7], 3, 1))
print(consecutive([1, 6, 9, -3, 4, -78, 0], -3, 4))
print(consecutive([1, 2, 3, 5], 2, 5))
