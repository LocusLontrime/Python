# accepted on codewars.com
def josephus(soldiers_nums: list, shift):
    current_index = 0
    result = []

    while len(soldiers_nums) > 0:

        current_index += shift - 1
        current_index %= len(soldiers_nums)

        soldier = soldiers_nums[current_index]

        print(f'current index: {current_index}, soldier: {soldier}, soldiers: {soldiers_nums}')

        result.append(soldier)
        soldiers_nums.pop(current_index)

    return result


print(josephus([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], 2))
print(josephus([True, False, True, False, True, False, True, False, True], 9))






