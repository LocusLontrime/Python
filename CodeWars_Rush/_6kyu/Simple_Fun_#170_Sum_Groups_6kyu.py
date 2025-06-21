# accepted on codewars.com

def sum_groups(arr: list):
    prev, curr = len(arr), 0
    arr_ = arr
    while prev != curr:
        new_arr = []
        i = 0
        while i < len(arr_):
            for remainder in [0, 1]:
                sum_ = 0
                while i < len(arr_) and arr_[i] % 2 == remainder:
                    sum_ += arr_[i]
                    i += 1
                if sum_ > 0:
                    new_arr += [sum_]
        arr_ = new_arr
        prev, curr = curr, len(arr_)
    return curr


test = [2, 1, 2, 2, 6, 5, 0, 2, 0, 5, 5, 7, 7, 4, 3, 3, 9]
test_case = [2, 1, 2, 2, 6, 5, 0, 2, 0, 3, 3, 3, 9, 2]

print(f'res -> {sum_groups(test)}')
