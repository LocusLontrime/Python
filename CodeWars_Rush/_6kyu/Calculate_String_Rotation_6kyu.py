# accepted on codewars.com
def shifted_diff(first, second):
    # code here!
    for i in range(len(first)):
        if first == second:
            return i
        first = first[-1] + first[:-1]
    return -1


print(f'{[1, 2, 3, 4, 5][:-1]}')

array = [1, 98, 989]
print(f'{list(enumerate(array))}')

