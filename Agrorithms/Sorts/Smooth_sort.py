def smooth_sort(array: list[int]):
    # generating leo nums for the array's given length
    leonardo_numbers = get_leonardo_numbers(len(array))
    # building a heap of leonardo heaps:
    pass


def get_leonardo_numbers(arr_length: int):
    leo_nums = []
    prev_leo, next_leo = 1, 1
    while prev_leo <= arr_length:
        leo_nums.append(prev_leo)
        prev_leo, next_leo = next_leo, prev_leo + next_leo + 1
    return leo_nums


def restore_heap():
    pass



