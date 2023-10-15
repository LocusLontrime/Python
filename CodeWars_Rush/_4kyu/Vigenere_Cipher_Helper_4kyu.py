# accepted on codewars.com
class VigenereCipher(object):

    def __init__(self, key, alphabet):

        self.alphabet = alphabet
        self.key = key

    def encode(self, text: str):

        return self.code(text)

    def decode(self, text):

        return self.code(text, False)

    def code(self, text, encode_or_not=True):

        result = ''

        for i in range(0, len(text)):

            if text[i] in self.alphabet:
                new_position = (self.alphabet.index(text[i]) + (1 if encode_or_not else -1) * self.alphabet.index(self.key[i % len(self.key)])) % len(self.alphabet)
                result += self.alphabet[new_position]
            else:
                result += text[i]

        return result
