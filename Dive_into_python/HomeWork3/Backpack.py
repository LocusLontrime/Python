# -*- coding: utf-8 -*-

# Создайте словарь со списком вещей для похода в качестве ключа и их массой в качестве значения.
# Определите какие вещи влезут в рюкзак передав его максимальную грузоподъёмность.
# Достаточно вернуть один допустимый вариант. *Верните все возможные варианты комплектации рюкзака.


things_for_expedition = {
    '1_pood_weight': 16,
    '2_pood_weight': 32,
    '4_pood_weight': 64,
    'i_pad_pro_m2_1tb': 1,
    'waterproof_tent': 8,
    'raincoat': 3,
    'warm_jacket': 7,
    'secret_password': 0,
    'railgun': 12,
    'secret_black_box': 24,
    'soap': 1,
    'boots': 3,
    'pistol': 2,
    'plasma_cannon': 72,
    'realms_rust_cannon': 1_000_000_000,
    'warm_sleeping_bag': 5
}

test = {
    '1': 1,
    '2': 2,
    '4': 4,
    '8': 8,
    '16': 16,
    '32': 32,
    '64': 64,
    '128': 128
}

WEIGHT_THRESHOLD = 90


def bacpack_valid_combs(things: dict):
    # aux pars:
    length = len(things)
    keys = list(things.keys())
    valid_combs = list()
    # full list of given things:
    print(f'things given: {keys}')

    # inner method:
    def recursive_seeker(current_item_comb: list, curr_weight: int, index: int):
        for i_ in range(index + 1, length):
            if (new_curr_weight := curr_weight + things[k := keys[i_]]) <= WEIGHT_THRESHOLD:
                valid_combs.append(new_current_item_comb := current_item_comb + [k])
                recursive_seeker(new_current_item_comb, new_curr_weight, i_)
    # recursive call:
    recursive_seeker([], 0, 0)
    # printing results:
    for i, valid_comb in enumerate(valid_combs):
        print(f'{i}-th valid comb: {valid_comb}')


bacpack_valid_combs(test)

bacpack_valid_combs(things_for_expedition)
