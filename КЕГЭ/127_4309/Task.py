# accepted on kompege.ru

# -*- coding: utf-8 -*-
# В саду N деревьев разных видов и возраста расположены в один ряд. Раз в неделю необходимо поливать деревья.
# Для полива деревьев используются поливальные машины. Одна машина едет с левой стороны, другая – с правой.
# Когда машина подъезжает к дереву, она выливает необходимое количество воды. На выливание 1 литра воды требуется 1 минута,
# на переезд между соседними деревьями – 5 минут. Количество воды, которым необходимо полить деревья, может отличаться,
# поэтому, если разместить воду в машины поровну, то вода в одной из машин может закончиться раньше и на полив всех деревьев уйдет больше времени.

# Напишите программу, которая поможет определить, сколько литров воды нужно загрузить в каждую машину, чтобы полив завершился как можно быстрее.

# Входные данные:
# Даны два входных файла (файл A и файл B),
# каждый из которых содержит в первой строке одно целое число N  – количество деревьев (1 ≤ N ≤ 105).
# Каждая из следующих N строк содержит целое число в диапазоне от 0 до 104 – количество литров воды,
# которым требуется полить деревья слева направо.

# Выходные данные:
# Вывести два целых числа – количество литров воды, которые необходимо разместить в левой машине сначала для файла А,
# затем для файла В. Если последний литр может быть вылит как левой, так и правой машиной без увеличения общей продолжительности полива,
# то его нужно погрузить в левую машину.

# Пример организации исходных данных во входном файле:
# [3, 1, 8, 3, 4]

# Для указанных входных данных в левую машину необходимо поместить 10 литров, в правую 9.
# Тогда итоговое время полива левой машины будет равно 3 + 5 + 1 + 5 + 6 = 20, правой машины 4 + 5 + 3 + 5 + 2= 19.


def calculate_volumes(array: list[int]) -> list[int]:
    TIME_DELAY = 5
    # array's length:
    n = len(array)
    # left water volume, right water volume = 0, 0
    volumes = [0, 0]
    volume_remained = sum(array)
    # the core algo:
    # left ind, right ind = 0, n - 1
    indices = [0, n - 1]
    # time_elapsed:
    times_elapsed = [0, 0]
    turn = 0  # 0 -> left, 1 -> right:
    while True:
        ind_, time_elapsed = indices[turn], times_elapsed[turn]
        # check for time remained:
        time_delay_ = TIME_DELAY * abs(indices[(turn + 1) % 2] - ind_)
        rem_litres = time_elapsed + array[ind_] - (times_elapsed[(turn + 1) % 2] + volume_remained - array[ind_] + time_delay_)
        if rem_litres > 0:
            # final volumes computation:
            volumes[(turn + 1) % 2] += volume_remained - array[ind_]
            volumes[turn] += array[ind_] - rem_litres
            # remained litres' partition:
            volumes[0] += rem_litres // 2 + (1 if rem_litres % 2 else 0)  # the last liter is always to the left car!
            volumes[1] += rem_litres // 2
            return volumes

        else:
            # time elapsed:
            times_elapsed[turn] += TIME_DELAY + array[ind_]
            # volume's change:
            volumes[turn] += array[ind_]
            volume_remained -= array[ind_]
            # index's walking:
            indices[turn] -= (1 if turn % 2 else -1)
            # next round:
            # turn = (turn + 1) % 2
            if times_elapsed[0] <= times_elapsed[1]:
                turn = 0
            else:
                turn = 1


def get_arr(file_name: str):
    arr_ = []
    with open(file_name, 'r') as f:
        arr_ = map(int, f.readlines()[1:])
        f.close()
    arr_ = list(arr_)
    return arr_


test_ex = [3, 1, 8, 3, 4]
arr_A = get_arr(f'27A_4309.txt')
arr_B = get_arr(f'27B_4309.txt')

print(f'test ex -> {calculate_volumes(test_ex)}')                                     # 36 366 98 989 98989 LL
print(f'file A -> {calculate_volumes(arr_A)}')
print(f'file B -> {calculate_volumes(arr_B)}')



