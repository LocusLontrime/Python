# Given a sorted array, output all triplets <a,b,c> such that a-b = c. Expected time is O(n^2).
# My approach using binary search took O(n^2 log(n)).
# When you attempt an approach, test your code with this example and list your outputs for verification.
# Thanks.
# -12, -7, -4, 0, 3, 5, 9, 10, 15, 16


def search_for_triplets(arr: list[int]) -> list[tuple[int, int, int]]:
    n = len(arr)
    values_set = set(arr)
    print(f'{values_set = }')

    triplets = []

    for j in range(n):
        for i in range(j + 1, n):
            if (diff := arr[j] - arr[i]) in values_set:
                if arr[j] != diff and arr[i] != diff:
                    triplets += [(arr[j], arr[i], diff)]
            elif (diff := arr[i] - arr[j]) in values_set:
                if arr[j] != diff and arr[i] != diff:
                    triplets += [(arr[j], arr[i], diff)]

    return triplets


test = [-12, -7, -4, 0, 3, 5, 9, 10, 15, 16]

print(f'res -> {search_for_triplets(test)}')
