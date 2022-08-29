# accepted on codewars.com
word_parts = "abcdefghijklmnopqrstuvwxyz'"


def top_3_words(text: str):
    text = text.lower()
    freq_dict = {}

    i = 0
    while i < len(text):
        curr_word = ''

        while i < len(text) and text[i] in word_parts:
            curr_word += text[i]
            i += 1

        if curr_word not in [' ', "'" * len(curr_word)]:
            if curr_word in freq_dict.keys():
                freq_dict[curr_word] += 1
            else:
                freq_dict[curr_word] = 1

        while i < len(text) and not text[i] in word_parts:
            i += 1

    print(freq_dict)

    freq_dict = sorted(freq_dict, key=freq_dict.get, reverse=True)

    print(freq_dict)

    if len(freq_dict) >= 3:
        return freq_dict[:3]
    elif len(freq_dict) == 2:
        return freq_dict[:2]
    elif len(freq_dict) == 1:
        return freq_dict[:1]
    else:
        return []


print(top_3_words('e e e e DDD ddd DdD: ddd ddd aa aA Aa, bb cc cC e e e'))
