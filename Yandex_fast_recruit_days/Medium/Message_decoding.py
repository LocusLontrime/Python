# accepted on coderun


def decode():
    s, n, words_encoded = get_pars()
    words = {get_hash(word): word for word in s}
    print(f'words: {words}')
    for word_encoded in words_encoded:
        print(f'{words[get_hash(word_encoded)]}')


def get_hash(word: str) -> int:                                                       # 36.6 98
    return hash(tuple((ord(word[i + 1]) - ord(word[i])) % 26 for i in range(len(word) - 1))) if len(word) > 1 else 0


def get_pars():
    s = input().split()
    n = int(input())
    words_encoded = [input() for _ in range(n)]
    return s, n, words_encoded


decode()



