# Write a method to determine if two strings are anagrams of each other.
# e.g. isAnagram("secure", "rescue") -> true
# e.g. isAnagram("conifers", "fir cones") -> true
# e.g. isAnagram("google", "facebook") -> false

def is_anagram(word1: str, word2: str) -> bool:
    letters_base1, letters_base2 = define_letter_base(word1), define_letter_base(word2)

    print(f'{letters_base1 = }')
    print(f'{letters_base2 = }')

    return letters_base1 == letters_base2


def define_letter_base(word: str) -> dict:
    letters_base = {}
    for letter in word:
        if letter not in letters_base:
            letters_base[letter] = 1
        else:
            letters_base[letter] += 1
    return letters_base


test = ('secure', 'rescue')

print(f'res -> {is_anagram(*test)}')

