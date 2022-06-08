def find_starting_index_of_num(number: int) -> int:
    length_of_number = len(str(number))
    power_of_ten = 10 ** (length_of_number - 1)

    return (length_of_number - 1) * power_of_ten - int('1' * (length_of_number - 1)) + length_of_number * (number - power_of_ten) if number > 9 else number - 1


print(find_starting_index_of_num(10))
print(find_starting_index_of_num(100))
print(find_starting_index_of_num(3536))


