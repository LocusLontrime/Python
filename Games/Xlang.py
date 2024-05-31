# éàçûãã ïàäîíêàôô (ïğàñòèòè (íåò) )


doubleable = []

# vowels:
prime_vowels = ['à', 'è', 'î', 'ó', 'û', 'ı']
vowels_pairs = {'à': 'î', 'î': 'à', 'è': 'å', 'å': 'è'}
composite_vowels = {'å': 'éı', '¸': 'éî', 'ş': 'éó', 'ÿ': 'éà'}

# consonants:
voiced_consonants = {'á', 'â', 'ã', 'ä', 'æ', 'ç', 'ë', 'ì', 'í', 'ğ'}  # [á], [â], [ã], [ä], [æ], [ç], [ë], [ì], [í], [ğ]
voiceless_consonants = {'ê', 'ï', 'c', 'ò', 'ô', 'x', 'ö', '÷', 'ø', 'ù'}  # [ê], [ï], [ñ], [ò], [ô], [õ], [ö], [÷], [ø], [ù]
consonants_pairs = {
    'ã': 'ê', 'á': 'ï', 'â': 'ô', 'ä': 'ò', 'ç': 'c', 'æ': 'ø',
    'ê': 'ã', 'ï': 'á', 'ô': 'â', 'ò': 'ä', 'c': 'ç', 'ø': 'æ'
}

# doubling:
doubleables = {'ô', 'ã', 'ö'}

# replacements:
replaceables = {'òñ': 'ö', 'ö': 'òñ'}

# omits:
omittables = {'é'}


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











































