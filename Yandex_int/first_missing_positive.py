def fmp(arr: list[int]) -> int:
    arr += [0, 0]
    length = len(arr)
    print(f'length: {length}')
    # let us get rid of negative ones:
    non_negatives = [num if 0 < num < length else 0 for num in arr]
    print(f'positives: {non_negatives}')
    # process them:
    for i, non_negative in enumerate(non_negatives):
        non_negatives[non_negative % length] += length
    print(f'processed array: {non_negatives}')
    # find the first missing positive:
    for i, processed_negative in enumerate(non_negatives):
        if processed_negative < length:
            return i


array = [5, 2, 1, 4, -7, 9, 7, 6, -3, 6, 17, 98, 3, 68, 18, 19, 99]
arr_x = [1, 2, 3]
arr_y = [1]
print(f'first missing positive: {fmp(array)}')
