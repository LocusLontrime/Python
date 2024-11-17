# precision of calculations:
import decimal

from decimal import Decimal

PREC_POWER = 1000

PRECISION = Decimal(f'1E-{PREC_POWER}')  # 1 * 10 ^ -1000

print(f'{PRECISION = }')                                                              # 36 36.6 366 98 989 98989 LL

decimal.getcontext().prec = PREC_POWER


def at_least_n_copies_per_m_summons_chance(n: int, m: int, base_chance: float = 1.6) -> float:
    """
    counts a chance to get at least n copies from n summons made
    if the base chance of getting the soul needed is given ->
    :param n: necessary amount of soul copies
    :param m: quantity of summons decided to make                                     # 36 366 98 989 98989 LL
    :param base_chance: chance of getting the banner soul per every summon
    :return: chance of getting at least n banner soul copies through m summons
    """
    # checks for invalid input:
    if n > m or n < 0:
        raise ValueError(f'n[{n}] cannot be greater than m[{m}] and n[{n}] must be greater than or equal to zero[{0}]')
    if n == 0:
        return 1.0
    # mathematical chance:
    base_ch = base_chance / 100  # 0.016
    # choose the best counting: from the n to the end                      
    # or from the beginning to n - 1 subtracted from 1 (for performance):
    start_i, end_i = (0, n - 1) if n < m - n else (n, m)
    # initial chance:
    ch_ = base_ch ** start_i * (1 - base_ch) ** (m - start_i) * combinations(m, start_i)
    ch_ = Decimal(ch_)
    # initial res value equals to zero:
    res = Decimal(0)
    # the core cycle of chance summation:
    counter = 0
    for copies_q in range(start_i, end_i + 1):
        if ch_ < PRECISION:
            # early break condition if we are already out of the PRECISION:
            break
        counter += 1
        res += ch_  # <-- summation itself
        # chance updating per cycle iteration:
        multiplier = Decimal(base_ch * (m - copies_q) / ((1 - base_ch) * (copies_q + 1)))
        ch_ *= multiplier
    print(f'{counter} ops done...')
    # result (depends on the counting direction):
    res = float(res)
    return 1 - res if n < m - n else res


def combinations(n: int, k: int) -> float:
    """
    counts quantity of combinations of n over k ->
    :param n: number of all items
    :param k: number of items in sample
    :return: number of combinations without repetitions
    """
    # performance check (needed for combs faster calcs but in our case k is always > n // 2...):
    k_ = k
    if k > n // 2:
        k_ = n - k
    res = 1
    # calculations itself:
    for multiplier in range(n, k_, -1):
        res *= multiplier / (multiplier - k_)
    # returns res:
    return res


def main():
    print(f'\n---------------------------------<Origin summon>--------------------------------------------------------')
    for k__, n__ in [(i, (7 - i) * 100) for i in range(4, -1, -1)]:
        print(f'chance at least [{k__, n__ = }] -> {at_least_n_copies_per_m_summons_chance(k__, n__) * 100:.{3}f} %')

    print(f'\n----------------------------------<Origin+5 summon>-----------------------------------------------------')
    for k__, n__ in [(i, (17 - i) * 100) for i in range(14, -1, -1)]:
        print(f'chance at least [{k__, n__ = }] -> {at_least_n_copies_per_m_summons_chance(k__, n__) * 100:.{3}f} %')

    print(f'\n----------------------------------<Origin A/D summon>-------------------------------------------------')
    for k__, n__ in [(i, (12 - i) * 100) for i in range(9, -1, -1)]:
        print(f'chance at least [{k__, n__ = }] -> {at_least_n_copies_per_m_summons_chance(k__, n__) * 100:.{3}f} %')

    print(f'\n----------------------------------<Origin+5 A/D summon>-----------------------------------------------')
    for k__, n__ in [(i, (22 - i) * 100) for i in range(19, -1, -1)]:
        print(f'chance at least [{k__, n__ = }] -> {at_least_n_copies_per_m_summons_chance(k__, n__) * 100:.{3}f} %')

    print(f'\n----------------------------------<Origin Chaos summon>-------------------------------------------------')
    for k__, n__ in [(i, (9 - i) * 100) for i in range(6, -1, -1)]:
        print(f'chance at least [{k__, n__ = }] -> {at_least_n_copies_per_m_summons_chance(k__, n__) * 100:.{3}f} %')

    print(f'\n----------------------------------<Origin+5 Chaos summon>-----------------------------------------------')
    for k__, n__ in [(i, (19 - i) * 100) for i in range(16, -1, -1)]:
        print(f'chance at least [{k__, n__ = }] -> {at_least_n_copies_per_m_summons_chance(k__, n__) * 100:.{3}f} %')

    amount_art_parts_to_origin = 3900

    coeff_ = (10 * 0.15 + 20 * 0.04 + 40 * 0.01) / 0.2
    num_ = int(amount_art_parts_to_origin / coeff_)
    print(f'{coeff_, num_ = }')

    print(f'{1500 * coeff_ = }')

    print(f'\n----------------------------------<Origin artefact summon>----------------------------------------------')
    for k__, n__ in [(num_, i) for i in list(range(500, 1500 + 100, 100)) + [2000] + [int((amount_art_parts_to_origin / coeff_) / 0.2)]]:
        print(f'chance at least [{k__, n__ = }] -> {at_least_n_copies_per_m_summons_chance(k__, n__, 20) * 100:.{10}f} %')
        print(f'...math expectation of artefact tickets -> {n__ * 0.2 * coeff_:.{0}f} / 3900')

    print(f'\n----------------------------------<Usual summon>--------------------------------------------------------')
    for i in range(1, 4 + 1 + 1):
        print(f'chance of getting at least {i} copy per 10 summons -> {(res_ := at_least_n_copies_per_m_summons_chance(i, 10, 4)) * 100:.{3}f} %')
        print(f'-> approx {1 / res_:.{0}f} summons for 1 encounter...')

    print(f'\n----------------------------------<Pick-up summon>--------------------------------------------------------')
    for i in range(1, 4 + 1 + 1):
        print(f'chance of getting at least {i} featured copy per 10 summons -> {(res_ := at_least_n_copies_per_m_summons_chance(i, 10, 1.6)) * 100:.{3}f} %')
        print(f'-> approx {1 / res_:.{0}f} summons for 1 encounter...')

    print(f'\n----------------------------------<Alchemy summon>--------------------------------------------------------')
    for i in range(1, 4 + 1 + 1):
        print(f'chance of getting at least {i} featured copy per 10 summons -> {(res_ := at_least_n_copies_per_m_summons_chance(i, 10, 2)) * 100:.{3}f} %')
        print(f'-> approx {1 / res_:.{0}f} summons for 1 encounter...')

    print(f'\n----------------------------------<Friendship summon>--------------------------------------------------------')
    for i in range(1, 4 + 1 + 1):
        print(f'chance of getting at least {i} copy per 10 summons -> {(res_ := at_least_n_copies_per_m_summons_chance(i, 10, 1)) * 100:.{3}f} %')
        print(f'-> approx {1 / res_:.{0}f} summons for 1 encounter...')

    # print(f'res O+2 -> {at_least_n_copies_per_m_summons_chance(6, 500)}')


if __name__ == '__main__':
    main()
