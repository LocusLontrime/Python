alphabet_eng = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"


def rot13_encoding(text: str) -> str:  # encoding ROT13
    return cesar_encoding(text, 13)


def rot13_decoding(text: str) -> str:  # decoding ROT13
    return cesar_encoding(text, -13)


def cesar_encoding(text: str, key: int) -> str:  # aux cesar method
    result = ''

    for ch in text.upper():
        if ch in alphabet_eng:
            result += alphabet_eng[(alphabet_eng.find(ch) + key) % len(alphabet_eng)]
        else:
            result += ch

    return result


# lower letters to lower and upper to upper ones, correct version
def cesar_encoding_save_the_case(text: str, key: int) -> str:  # aux cesar method
    result = ''

    for ch in text:

        curr_ch = ch.upper()

        if curr_ch in alphabet_eng:

            expr = alphabet_eng[(alphabet_eng.find(curr_ch) + key) % len(alphabet_eng)]

            result += (expr if not ch.islower() else expr.lower())
        else:
            result += ch

    return result


print(cesar_encoding('Why are you going to go there?..', 13))

print(rot13_encoding('Why are you going to go there?..'))

print(rot13_decoding(rot13_encoding('Why are you going to go there?..')))

