# accepted on codewars.com
import collections
import time


def list_position(word):
    """Return the anagram list position of the word"""
    chars_occurrences_dict = get_freq_dict(word)
    # print(f'chars_occurrences_dict: {chars_occurrences_dict}')
    position_number = 0
    for i in range(len(word), 0, -1):
        position_number += permutations_with_repetitions(chars_occurrences_dict, i, word[len(word) - i])
        if chars_occurrences_dict[word[len(word) - i]] > 1:
            chars_occurrences_dict[word[len(word) - i]] -= 1
        else:
            del chars_occurrences_dict[word[len(word) - i]]
            chars_occurrences_dict = dict(sorted(chars_occurrences_dict.items(), key=lambda x: x[0]))
    return position_number + 1


def get_freq_dict(word):
    chars_occurrences_dict = collections.OrderedDict()
    for char in word:
        if char in chars_occurrences_dict.keys():
            chars_occurrences_dict[char] += 1
        else:
            chars_occurrences_dict[char] = 1
    return dict(sorted(chars_occurrences_dict.items(), key=lambda x: x[0]))


def permutations_with_repetitions(chars_occurrences_dict, k, char):
    result = rec_fact(k - 1, 1) * get_elements_quantity_before(chars_occurrences_dict, char)
    for value in chars_occurrences_dict.values():
        result //= rec_fact(value, 1)
    return result


def get_elements_quantity_before(chars_occurrences_dict, char):
    counter = 0
    for key, value in chars_occurrences_dict.items():
        if key == char:
            return counter
        else:
            counter += value
    return counter


def rec_fact(n, res):
    return res if n == 0 else rec_fact(n - 1, res * n)


print(get_freq_dict("HYUUTTRKSJFJGUTJDJCSSNMHYUUTTRKSJFJGUTJDJCSSNMHYUUTTRKSJFJGUTJEDJCISSNMHYUUTTRKSJFJGUTJED" +
            "JCISSMYUUTTRKSJFJGUTJEDJCISSNYUUTTRKSJFJGUTJEDJCISSNMHYUUTTRKSJFJUTJEDJCISSNMHYUUTTRKSJFJGUTJEDJCISSNMHYUUTTRKSJFJGU" +
            "TJEDJCISSMHYUUTTRKSJFJGUTJEDJCISSNMHUUTTRKSJFJGUTJEDJCISSNMHYUUTTRKSJFJUTJEDJCISSNMHYUUTTRKSJFJGUTJEDJCISSNMHYUUTTRKSJ" +
            "JGUTJEDJCISSNMHYUUTTRKSJJGUTJEDJCISSNMHUUTTRKSJFJGUTJEDJCSSNMYUUTTRKSJFJGUTJEDJCISSNMHYUUTTRKSJFJGUTJEDJCISSNMHYUUTT" +
            "KSJFJGUTJEDJCISSHYUUTTRKSJFJGUTJEDJCISSNMHUUTTRKSJJGUTJEDJCISSNMHYUUTTRKSJFJGUTJEDJCISSNMHYUUTTRKSJFJGUTJEDJCISSNMHY" +
            "UUTTKSJFJGUTJEDJCISSNMHYUUTTSJFJGUTJEDJCISSNMHYUUTTRKSJFJGUTJEDJCISSNMHYUUTTRKSJFJGUTJEDJCISSNMHYUUTTRKSJFJGUTJEDJCISS" +
            "NMHYUUTTRKSJFJGUTJEDJCISSNMHYUUTTRKSJFJGUTJEDJCISSNMHYUUTTRKSJFJGUTJEDJCISSNMHYUUTTRKSJFJGUTJEDJCISSNMHYUUTTRKSJFJGUTJEDJ" +
            "ISSNMHYUUTTRKSJFJGUTJEDJCISSNMHYUUTTRKSJFJGUTJEDJCISSNMHYUUTTRKSJFJUTJEDJCISSNMHYUUTTRSJFJGUTJEDJCISSNMHYUUTTRKSJFJGUT" +
            "JDJISSNMHYUUTTRSJFJGUTJEDJISSN"))


large_one = "MHYUUTTRKSJFJGUTJEDJCISSNMHYUUTTRKSJFJGUTJEDJCISSNMHYUUTTRKSJFJGUTJEDJCISSNMHYUUTTRKSJFJGUTJEDJCISSNMHYUUTTRKSJFJGUTJEDJCISSNMHYUUTTRKSJFJGUTJEDJCISSNMHYUUTTRKSJFJGUTJEDJCISSNMHYUUTTRKSJFJGUTJEDJCISSNMHYUUTTRKSJFJGUTJEDJCISSNMHYUUTTRKSJFJGUTJEDJCISSNMHYUUTTRKSJFJGUTJEDJCISSNMHYUUTTRKSJFJGUTJEDJCISSNMHYUUTTRKSJFJGUTJEDJCISSNMHYUUTTRKSJFJGUTJEDJCISSNMHYUUTTRKSJFJGUTJEDJCISSNMHYUUTTRKSJFJGUTJEDJCISSNMHYUUTTRKSJFJGUTJEDJCISSNMHYUUTTRKSJFJGUTJEDJCISSNMHYUUTTRKSJFJGUTJEDJCISSNMHYUUTTRKSJFJGUTJEDJCISSNMHYUUTTRKSJFJGUTJEDJCISSNMHYUUTTRKSJFJGUTJEDJCISSNMHYUUTTRKSJFJGUTJEDJCISSNMHYUUTTRKSJFJGUTJEDJCISSNMHYUUTTRKSJFJGUTJEDJCISSNMHYUUTTRKSJFJGUTJEDJCISSNMHYUUTTRKSJFJGUTJEDJCISSNMHYUUTTRKSJFJGUTJEDJCISSNMHYUUTTRKSJFJGUTJEDJCISSNMHYUUTTRKSJFJGUTJEDJCISSNMHYUUTTRKSJFJGUTJEDJCISSNMHYUUTTRKSJFJGUTJEDJCISSNMHYUUTTRKSJFJGUTJEDJCISSNMHYUUTTRKSJFJGUTJEDJCISSNMHYUUTTRKSJFJGUTJEDJCISSNMHYUUTTRKSJFJGUTJEDJCISSNMHYUUTTRKSJFJGUTJEDJCISSNMHYUUTTRKSJFJGUTJEDJCISSNMHYUUTTRKSJFJGUTJEDJCISSN"
start = time.time_ns()
print(list_position(large_one))
finish = time.time_ns()
print(f'time elapsed: {(finish - start) // 10 ** 6} milliseconds')
