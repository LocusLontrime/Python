def shorten(str_list: list[str]) -> list[str]:
    str_list = sorted(str_list, key=len)
    result_list = []

    print(f'sorted str list: {str_list}')

    for string in str_list:

        n = 1
        while len(string) - 2 * n > 1:
            prefix = string[:n]
            suffix = string[-n:]

            possible_string_representation = prefix + str(len(string) - 2 * n) + suffix

            if possible_string_representation in result_list:
                if len(string) - 2 * n in [2, 3]:
                    result_list.append(string)
                    break
                else:
                    n += 1
            else:
                result_list.append(possible_string_representation)
                break

    return result_list


arr = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
print(arr[:3])
print(arr[:-3])
print(arr[-3:])

list_of_strings = ["localization", "internationalization"]
list_of_strings_2 = ["banana", "bugaga", "blabla", "apple", "astre", "potato", "tomato"]
print(shorten(list_of_strings))
print(shorten(list_of_strings_2))