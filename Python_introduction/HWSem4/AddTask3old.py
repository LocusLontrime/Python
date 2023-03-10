from functools import reduce


def get_sum_from_file(path_to_file: str) -> int:
    with open(path_to_file, "r") as file:
        numbers_str_list = file.readlines()
        sum_of_numbers = reduce(lambda x, y: int(x) + int(y), numbers_str_list)

    return int(str(sum_of_numbers)[:10])


print(get_sum_from_file('Numbers.txt'))

