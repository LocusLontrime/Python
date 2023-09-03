def longest_common_part(words: list[str]) -> str:
    common_part = words[0]  # we can do this so as the initial array contains at least one word!
    for word in words:
        for i in range(min(len(common_part), len(word))):
            if common_part[i] != word[i]:
                slice_i = i
                break
        else:
            continue
        common_part = word[:slice_i]
    return common_part


def lcp(words: list[str]) -> str:
    common_part = ''
    for letters in zip(*words):
        if len(set(letters)) == 1:
            common_part += letters[0]
        else:
            return common_part


words_ = ['hour', 'house', 'hook', 'hovercraft', 'horror', 'homogenisation', 'hybrid', 'hologram']

print(f'common part: {longest_common_part(words_)}')

print(f'zip: {list(zip(*words_))}')

print(f'common part zip: {lcp(words_)}')



