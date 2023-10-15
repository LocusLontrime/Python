# accepted on codewars.com
def two_sum(numbers, target):
    occurrences = {}
    for i, num_ in enumerate(numbers):
        if (n2 := target - num_) in occurrences.keys():
            return i, occurrences[n2]
        occurrences[num_] = i


arr = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
t = 13

print(f'res: {two_sum(arr, t)}')
