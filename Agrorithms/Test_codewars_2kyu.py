def find_starting_index_of_num(number: int) -> int:
    length_of_number = len(str(number))
    power_of_ten = 10 ** (length_of_number - 1)

    return (length_of_number - 1) * power_of_ten - int('1' * (length_of_number - 1)) + length_of_number * (number - power_of_ten) if number > 9 else number - 1


# print(find_starting_index_of_num(10))
# print(find_starting_index_of_num(100))
# print(find_starting_index_of_num(3536))

list_of_nums = [1, 2, 3, 4, 5, 6, 7]

new_list_of_nums = list_of_nums.copy()

list_of_nums.append(9)

print(f'list of nums: {list_of_nums}')
print(f'new list of nums: {new_list_of_nums}')


