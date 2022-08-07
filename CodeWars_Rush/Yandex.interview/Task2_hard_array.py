def find_most_freq_element(string_array: str):
    freq_dict = {}
    curr_num_str = ''

    i = 0
    while i < len(string_array):
        curr_num_str = ''
        while i < len(string_array) and string_array[i].isdigit():
            curr_num_str += string_array[i]
            i += 1

        print(f'curr num str: {curr_num_str}')

        if curr_num_str != '':
            number = int(curr_num_str)
            if number not in freq_dict:
                freq_dict[number] = 1
            else:
                freq_dict[number] += 1

        while i < len(string_array) and not string_array[i].isdigit():
            i += 1

    max_freq = max(freq_dict.values())
    result_list = []

    for key in freq_dict.keys():
        if freq_dict[key] == max_freq:
            result_list.append(key)

    return sorted(result_list)


arr_str = "[1, 2, 2, 2, 3, 5, [5, 5], 6, [7, 8, 9, [10, 11]]]"
print(find_most_freq_element(arr_str))
