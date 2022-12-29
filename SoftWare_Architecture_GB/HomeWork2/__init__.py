import random

import GoldGenerator, GemsGenerator
generators_list = []

def create_generators_list(l_border: int, r_border: int):
    generators_list.append(GoldGenerator.GoldGenerator(l_border, r_border))
    generators_list.append(GemsGenerator.GemsGenerator(l_border, r_border))

create_generators_list(1, 100)


for i in range(10):
    print(f'LALA')
    k = random.randint(0, 1)
    generators_list[k].open_reward()


