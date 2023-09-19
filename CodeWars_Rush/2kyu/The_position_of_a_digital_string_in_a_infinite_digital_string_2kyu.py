# accepted on codewars.com
def find_position(num_string):  # accepted on codewars.com
    # the min positions index for all the partitions of number given
    entries_indexes = []

    # finds the index of beginning of the number given in the infinity consecutive naturals sequence
    def find_starting_index_of_num(number: int) -> int:

        length_of_number = len(str(number))
        power_of_ten = 10 ** (length_of_number - 1)

        # just a math formula from a row sum (for nums less than max power of ten before number given) and the remained lengths that are all the same (= length of number given)
        return (length_of_number - 1) * power_of_ten - int('1' * (length_of_number - 1)) + length_of_number * (number - power_of_ten) if number > 9 else number - 1

    # finds the min index of the current num partition entry
    def find_entry_index(beg_ind: int, length_of_num: int) -> int:

        # if the number is divided by some parts and one of them is the whole one
        if length_of_num + beg_ind <= len(num_string):

            pivot_num = int(num_string[beg_ind: beg_ind + length_of_num])

            print(f'pivot num = {pivot_num}, beg_ind = {beg_ind}, length = {length_of_num}')

        else:  # number is divided by two parts and both of them are parts of two consecutive elements in an infinite sequence
            # situation: num = left_num_part|right_num_part -> ###left_num_part|right_num_part@@@@, where ### - left part of the whole left_num and
            # @@@@ - right one of the whole right_num

            left_num_part = num_string[:beg_ind]  # left and right parts of elements the number given consists of
            right_num_part = num_string[beg_ind:]

            print(f'left_num_part = {left_num_part}, right_num_part = {right_num_part}, beg_ind = {beg_ind}, length = {length_of_num}')

            right_rem_length = beg_ind + length_of_num - len(num_string)  # length of @@@@ part

            slice_of_left_num_part = left_num_part[-right_rem_length:]  # the @@@@ part itself

            print(f'slice_of_left_num_part = {slice_of_left_num_part}')

            if slice_of_left_num_part == '9' * right_rem_length:  # the problem of 99...999 part
                pivot_num = int(right_num_part + ('0' * right_rem_length))  # then we must change the right num
            else:
                pivot_num = int(right_num_part + slice_of_left_num_part) + 1  # simple way

            print(f'piv_el = {pivot_num}')
            print(f'slice: {str(pivot_num - 1)[-beg_ind:]}, left_num_part = {left_num_part}')

            if str(pivot_num - 1)[-beg_ind:] != left_num_part:  # if the two elements is not consecutive ones -> we must return -1
                return -1

        expected_consecutives = ''
        sequence_length = 0

        if beg_ind != 0:

            if str(pivot_num - 1)[-beg_ind:] != num_string[:beg_ind]:  # here we check the left tail of an element
                return -1  # -1 if the tail is wrong

            else:  # if not we proceed to the right (to the beginning of pivot num)
                expected_consecutives += num_string[:beg_ind]
                sequence_length += beg_ind

        current_num = pivot_num

        while sequence_length < len(num_string):  # here we continue moving through the presumably consecutive items till the end of cycle (while we  are still in the len of num_string

            if sequence_length + len(str(current_num)) < len(num_string):
                expected_consecutives += str(current_num)
                sequence_length += len(str(current_num))
            else:
                expected_consecutives += str(current_num)[:len(num_string) - sequence_length]  # here the current number get sliced coz the current length of expected_consecutive may exceed the len of num_string
                sequence_length = len(num_string)

            current_num += 1  # iterating through the consecutive ones

        print(f'expected_consecutives = {expected_consecutives}')

        if expected_consecutives != num_string:  # if expected string differs from the num_string given
            return -1

        return find_starting_index_of_num(pivot_num) - beginning_index  # we must subtract the beginning index from position of pivot_num in the infinite sequence to proceed to the correct position of the num_string

    for number_length in range(0, len(num_string) + 1):  # the cycling all over the necessary partitions of the num_string
        for beginning_index in range(number_length):

            curr_index = find_entry_index(beginning_index, number_length)

            if curr_index >= 0:  # we should not add -1 indexes to prevent the incorrect answer
                entries_indexes.append(curr_index)

    # the case of zero entries_indexes list
    if len(entries_indexes) == 0:
        return find_starting_index_of_num(int('1' + num_string)) + 1

    # searching for the min index to get the result
    return min(entries_indexes)


print(find_position('112131'))
print(find_position('111'))
print(find_position('53635'))
print(find_position('555899959741198'))
print(find_position('00101'))
print(find_position('00'))

# print([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11][3: 3 + 3])
#
# print([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11][3:])
# print([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11][:3])
#
# print([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11][-3:])
#

# print([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11][-1:])
# print([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11][:1])

