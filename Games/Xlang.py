# ������ ��������� (�������� (���) )


doubleable = []

# vowels:
prime_vowels = ['�', '�', '�', '�', '�', '�']
vowels_pairs = {'�': '�', '�': '�', '�': '�', '�': '�'}
composite_vowels = {'�': '��', '�': '��', '�': '��', '�': '��'}

# consonants:
voiced_consonants = {'�', '�', '�', '�', '�', '�', '�', '�', '�', '�'}  # [�], [�], [�], [�], [�], [�], [�], [�], [�], [�]
voiceless_consonants = {'�', '�', 'c', '�', '�', 'x', '�', '�', '�', '�'}  # [�], [�], [�], [�], [�], [�], [�], [�], [�], [�]
consonants_pairs = {
    '�': '�', '�': '�', '�': '�', '�': '�', '�': 'c', '�': '�',
    '�': '�', '�': '�', '�': '�', '�': '�', 'c': '�', '�': '�'
}

# doubling:
doubleables = {'�', '�', '�'}

# replacements:
replaceables = {'��': '�', '�': '��'}

# omits:
omittables = {'�'}


# TODO: words dictionary is badly needed...

# some rules (briefing):
# 1. unstressed vowels can be replaced by pairs from vowels_pairs dictionary if they exist... (stress dictionary needed)
# 2. composite vowels can be replaced by their transcription pairs from composite_vowels dict...
# 3. voiceless consonants can be replaced by their voiced equivalents and vice versa  (???) if they are followed by another voiceless consonant /
# they are situated in the end of the word...
# 4. some consonants in the end of the word can be doubled if they lies in doubleables set...
# 5. some parts can be replaced by another ones -> replaceables dict is created for this purpose...
# 6. some letters can be omitted in some cases: omittables set...
# 7. some several words can be connected in the bigger one (when ???)
#
#
#



class Word:
    def __init__(self):
        ...


class Mutation:
    def __init__(self):
        ...


def translate(word: str) -> str:
    ...











































