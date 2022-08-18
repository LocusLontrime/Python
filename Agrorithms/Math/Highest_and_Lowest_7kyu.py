def high_and_low(numbers: str):
    array_of_numbers = numbers.split(' ')
    return f'{max(array_of_numbers)} {min(array_of_numbers)}'


print(high_and_low("1 2 3 4 5"))  # return "5 1"
print(high_and_low("1 2 -3 4 5"))  # return "5 -3"
print(high_and_low("1 9 3 4 -5"))  # return "9 -5


