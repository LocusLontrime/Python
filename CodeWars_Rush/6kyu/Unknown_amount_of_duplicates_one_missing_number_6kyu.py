# accepted on codewars.com
def find_dups_miss(arr: list[int]):
    numbers_dict = dict()
    dups = set()
    for el in arr:
        if el in numbers_dict.keys():
            # means a duplicate been found or appeared again
            numbers_dict[el] = 1
            dups.add(el)
        else:
            # the first appearance of element
            numbers_dict[el] = 0
    # elements set
    uniq = numbers_dict.keys()
    max_one, min_one = max(uniq), min(uniq)
    # searching for the missing one
    for num in range(min_one, max_one + 1):
        if num not in uniq:
            uniq = num
            break
    # dups should be sorted
    return [uniq, sorted(dups)]


arr1 = [10, 9, 8, 9, 6, 1, 2, 4, 3, 2, 5, 5, 3]
arr2 = [20, 19, 6, 9, 7, 17, 16, 17, 12, 5, 6, 8, 9, 10, 14, 13, 11, 14, 15, 19]
arr3 = [24, 25, 34, 40, 38, 26, 33, 29, 50, 31, 33, 56, 35, 36, 53, 49, 57, 27, 37, 40, 48, 44, 32, 35, 45, 52, 43, 47,
        26, 51, 55, 28, 41, 42, 46, 51, 25, 30, 44, 54]

print(find_dups_miss(arr3))
