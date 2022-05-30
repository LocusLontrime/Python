# (Locus_Lontrime HW) Сформировать список из N членов последовательности. Для N = 5: 1, -3, 9, -27, 81 и т.д.

def get_first_n_members_of_seq(length):
    list = []
    pow = 1

    for i in range(0, length):
        list.append(pow)
        pow *= -3

    return list


print(get_first_n_members_of_seq(8))
