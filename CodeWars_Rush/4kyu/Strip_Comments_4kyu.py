# accepted on codewars.com
def strip_comments(strng: str, markers: list[str]):
    strings = strng.split('\n')
    res = ''

    for string in strings:
        min_marker_index = len(string)
        for marker in markers:
            if marker in string:
                curr_marker_index = string.index(marker)
                min_marker_index = min(min_marker_index, curr_marker_index)

        res += string[:min_marker_index].rstrip() + '\n'

    return res[:-1]


print(strip_comments('apples, pears # and bananas\ngrapes\nbananas !apples', ['#', '!']))

