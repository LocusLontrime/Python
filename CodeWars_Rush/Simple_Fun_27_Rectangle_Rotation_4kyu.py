# accepted on codewars.com
import math


def rectangle_rotation(a, b):  # 36 366 98 989

    aux_a = math.floor(a / math.sqrt(2))
    aux_b = math.floor(b / math.sqrt(2))

    side_a_1 = aux_a if aux_a % 2 == 0 else aux_a - 1
    side_a_2 = aux_a if aux_a % 2 != 0 else aux_a - 1

    side_b_1 = aux_b if aux_b % 2 == 0 else aux_b - 1
    side_b_2 = aux_b if aux_b % 2 != 0 else aux_b - 1

    print(f'side_a_1: {side_a_1}, side_a_2: {side_a_2}, side_b_1: {side_b_1}, side_b_2: {side_b_2}')

    return (side_a_1 + 1) * (side_b_1 + 1) + (side_a_2 + 1) * (side_b_2 + 1)


print(rectangle_rotation(6, 4))


