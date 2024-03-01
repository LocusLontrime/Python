# accepted on https://informatics.msk.ru/mod/statements/view.php?id=1459#1
memo_table = {}


def get_spell_power(spell: str, magic_word: str) -> int:
    return rec_core(0, 0, len(spell), len(magic_word), spell, magic_word)


def rec_core(j: int, i: int, max_j: int, max_i: int, spell: str, magic_word: str) -> int:

    # border cases:
    if i == max_i:
        # case 2 -> secret magic word found:
        return 1

    if j >= max_j:
        # case 1 -> out of spell:
        return 0

    # body of rec:
    if (j, i) not in memo_table.keys():
        res = 0

        for ind in range(j, max_j):  # secret words only, letters cannot be consecutive...
            # recurrent relation:
            if spell[ind] == magic_word[i]:
                res += rec_core(ind + 2, i + 1, max_j, max_i, spell, magic_word)

        memo_table[(j, i)] = res

    return memo_table[(j, i)]


# examples:
# spell_ = "azaazazzaazzazaazazzaazzazaazazzaazzazaazazzaazzazaazazzaazzazaazazzaazz"
# magic_word_ = "azazazazazaz"
spell_ = input()
magic_word_ = input()
print(f'{get_spell_power(spell_, magic_word_)}')
