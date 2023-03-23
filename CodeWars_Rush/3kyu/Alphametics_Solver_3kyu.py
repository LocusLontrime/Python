# accepted on codewars.com -->> TODO: NEEDS SOME OPTIMIZATION!!!

import time
from functools import reduce  # LL 36 366 98 989

rec_counter: int
finishing_counter: int


def alphametics(puzzle: str) -> str:
    global rec_counter, finishing_counter

    BASE = 10

    def get_words():
        """
        gets words split
        """
        l, r = puzzle.replace(' ', '').split('=')
        return l.split('+'), r

    def to_int(word: str, seq: dict):
        """
        calculates the int representation of the word given, using a special dictionary 'seq'
        """
        return reduce(lambda x, y: 10 * x + seq[y], word, 0)

    rec_counter = 0
    finishing_counter = 0

    summands, sum_ = get_words()
    length = len(sum_)

    # growing list of digits_permutation:
    dig_perms = [dict()]
    # aux digits_permutation list, needed for every iteration of the main cycle:
    new_dig_perms = []

    # aux dictionary for rec method:
    uniq_digs_per_curr_len = dict()
    # aux pars:
    curr_uniq_digs = set()
    new_uniq_digs: list[str]

    for i in range(length):
        new_uniq_digs = []

        for summand in summands:
            if i < len(summand):
                el = summand[len(summand) - 1 - i]
                if el not in curr_uniq_digs:
                    new_uniq_digs.append(el)
                curr_uniq_digs.add(el)

        el = sum_[length - 1 - i]
        if el not in curr_uniq_digs:
            new_uniq_digs.append(el)
        curr_uniq_digs.add(el)

        # TODO: deal with 'curr_uniq_digs.copy()', is it really needed or should be excluded from tuple?..
        uniq_digs_per_curr_len[i] = len(curr_uniq_digs), curr_uniq_digs.copy(), new_uniq_digs
    print(f'uniq_digs_per_curr_len: {uniq_digs_per_curr_len}')

    # consecutive letters:
    letters = []
    for _ in range(len(sum_)):
        letters += uniq_digs_per_curr_len[_][2]

    # the letters that cannot be equal to zero:
    forbidden_letters = set([_[0] for _ in summands] + [sum_[0]])

    # permutations restriction:
    possible_digits = None
    letter = None
    if max(len(_) for _ in summands) < len(sum_):
        counter = sum([1 for _ in summands if len(_) == len(sum_) - 1])
        possible_digits = [_ for _ in range(counter + 1)]
        letter = sum_[0]

    print(f'letters: {letters}')
    print(f'forbidden_letters: {forbidden_letters}')

    # the longest word's iterator:
    curr_len = 0

    # main logic:
    def recursive_seeker(sequence: dict[str, int], curr_seq_len: int, threshold_len: int, left_: list[str],
                         right_: str):
        global rec_counter, finishing_counter
        rec_counter += 1

        # base case:
        if curr_seq_len == threshold_len:
            finishing_counter += 1
            # checks math expression of length 'curr_seq_len':
            reduced_left_part = reduce(lambda x, y: x + to_int(y, sequence), left_, 0)
            if reduced_left_part % (10 ** (1 + curr_len)) == to_int(right_, sequence):
                new_dig_perms.append(sequence)
            return
        # here the sequence starts building:
        curr_letter = letters[curr_seq_len]
        for digit in (range(BASE) if letter is None else range(BASE) if curr_letter != letter else possible_digits):
            if digit not in sequence.values() and not (digit == 0 and curr_letter in forbidden_letters):
                # dictionary extending:
                sequence_ = sequence.copy()
                sequence_[curr_letter] = digit
                recursive_seeker(
                    sequence_,
                    curr_seq_len + 1,
                    threshold_len,
                    left_,
                    right_
                )

    # now cycling through the max word length:
    # TODO: Forbid the leading zeroes, memoization, early break, pay attention to the most significant digit (can be exactly 1 at instance)
    while curr_len < len(sum_):
        print(f'curr_len: {curr_len}')
        # print(f'dig_perms: {dig_perms}')
        new_dig_perms = []
        left, right = [_[-(1 + curr_len):] for _ in summands], sum_[-(1 + curr_len):]
        print(
            f'perms quantity: {len(dig_perms)}, curr_seq_len: {uniq_digs_per_curr_len[curr_len - 1][0] if curr_len else 0}, '
            f'threshold_len: {uniq_digs_per_curr_len[curr_len][0]}, rec_counter: {rec_counter}, finishing_counter: {finishing_counter}')
        for _, perm in enumerate(dig_perms):
            recursive_seeker(
                perm,
                uniq_digs_per_curr_len[curr_len - 1][0] if curr_len else 0,
                uniq_digs_per_curr_len[curr_len][0],
                left,
                right
            )
        dig_perms = new_dig_perms[:]
        curr_len += 1

    print(f'rec_counter: {rec_counter}, finishing_counter: {finishing_counter}')
    print(f'found {len(dig_perms)} possible permutations...')
    # print(f'possible perms: {dig_perms}')

    solution = dig_perms[0]
    print(
        s := f'SOL: {solution} --> {" + ".join(str(to_int(summand, solution)) for summand in summands)} = {str(to_int(sum_, solution))}')
    return s


# INPUT:    "SEND + MORE = MONEY"
# SOLUTION: "9567 + 1085 = 10652"
# solution_ = alphametics("SEND + MORE = MONEY")
# s_ = alphametics("ELEVEN + NINE + FIVE + FIVE = THIRTY")
# s__ = alphametics("COUPLE + COUPLE = QUARTET")
# _s_ = alphametics("OPPPPPPP + OOPPPPPP + OOOPPPPP + OOOOPPPP + OOOOOPPP + OOOOOOPP + OOOOOOOP = ERTYUIOP")
# alphametics("SATURN + URANUS + NEPTUNE + PLUTO = PLANETS")
# alphametics("RMI + IQB + EMBM = ZRZB")


start = time.time_ns()
alphametics("XNX + NAPXPXN + GNLQAQ + ALGXGPN + VQAGAP + VQPPI = VPGNVVNO")
# alphametics("SEND + MORE = MONEY")
# alphametics("UEA + YXBFU + HDGY + EGEDXGH + HAHYB = EUEABYU")
# alphametics("OZ + CMD = CJK")
# alphametics("WSFAF + ONRF + UTTURR + WSSSUOO + OSONTROO = OFNFAZWW")
# alphametics("EGXWFY + GZLGYW + WLXZLWG + ZWLAGHX + HAHHG = GLFGHYFE")
# alphametics("UUM + TALNR + ANKMNH + AURMMUMA + HUTTTLL = NNNNMMLA")
# alphametics("HCGHU + MMEGH + GEYKT + TYECEE = ZUZZZCK")
# alphametics("HTH + HATSH + ZADHB + PPBSAZ + ZPHT = DDKTDSH")
# alphametics("RC + SRE + WRTEEC + SSWEWR + CUTTICSU = CWCSROEZ")
# alphametics("FIWVFX + WFPVX + YXY + SLSWP + SLWIXWX = YXFXPPF")
# alphametics("SDWPH + PMHMDW + DSHE + CPCPCW + MHWEHWPC = MWEDSRWE")
# alphametics("SJQCC + SBJJKOQ + SQXPXS + CBLP + XSCCB = SKSCLQO")
# alphametics("AACO + AACT + AACO + AACC + AACC + AAOC = CBAXO")
# alphametics("NJJJJW + NNNWWA + NJGZG + NNKKKJKL + ZJAQWUGG = LZZLNKNGN")
# alphametics("ZZPYBD + YUBBD + DGBGBYQ + DGDDSYB + ZQQUN = BPQGQPBU")
# alphametics("WMMVQH + LLVH + TSBM + STTSQWU + THSQBMSM = LUSLMSBV")
# alphametics("XNX + NAPXPXN + GNLQAQ + ALGXGPN + VQAGAP + VQPPI = VPGNVVNO")
# alphametics("NN + MCXHQ + HGH + GMHCY + MQGQHYN = MNNCNYN")
# alphametics("ESSE + ANCE + UZEX + UCNAC + JSCBA = EENUBU")
# alphametics("SATURN + URANUS + NEPTUNE + PLUTO = PLANETS")
# alphametics("OPPPPPPP + OOPPPPPP + OOOPPPPP + OOOOPPPP + OOOOOPPP + OOOOOOPP + OOOOOOOP = ERTYUIOP")
# alphametics("PJRJPJ + UYY + PWOOOOP + YUGGOG + MHRUY = OJGRYUP")
# alphametics("IC + EBYVEC + III + CKEBK + CKGIVYEV = CBEQEYYK")
# alphametics("BRZZNN + NBNKR + UNRBBQ + RNDTZQR + ZUDQ = ZUDUUQZ")
finish = time.time_ns()
print(f'time elapsed: {(finish - start) // 10 ** 6} ms')

# list_ = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
# print(f'lala')
# print(f'list slice: {list_[-2:]}')
#
# print(f'contagious'[-2:])
#
# seq_ = {'A': 1, 'B': 2, 'C': 4, 'E': 9}
#
# word_ = 'ABEC'
#
# print(f'reduced word: {reduce(lambda x, y: 10 * x + seq_[y], word_, 0)}')
