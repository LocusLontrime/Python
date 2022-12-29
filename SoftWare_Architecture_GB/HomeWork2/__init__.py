import random

import GoldGenerator, GemsGenerator, BronzeGenerator, CopperGenerator, IronGenerator, LumberGenerator, PlatinumGenerator, SilverGenerator, StoneGenerator, SulphurGenerator
generators_list = []

def create_generators_list(l_border: int, r_border: int):
    generators_list.append(GoldGenerator.GoldGenerator(l_border, r_border))
    generators_list.append(GemsGenerator.GemsGenerator(l_border, r_border))
    generators_list.append(BronzeGenerator.BronzeGenerator(l_border, r_border))
    generators_list.append(CopperGenerator.CopperGenerator(l_border, r_border))
    generators_list.append(IronGenerator.IronGenerator(l_border, r_border))
    generators_list.append(LumberGenerator.LumberGenerator(l_border, r_border))
    generators_list.append(PlatinumGenerator.PlatinumGenerator(l_border, r_border))
    generators_list.append(SilverGenerator.SilverGenerator(l_border, r_border))
    generators_list.append(StoneGenerator.StoneGenerator(l_border, r_border))
    generators_list.append(SulphurGenerator.SulphurGenerator(l_border, r_border))


create_generators_list(1, 100)


for i in range(100):
    k = random.randint(0, 9)
    generators_list[k].open_reward()

print(dir('AmberCode.SoftWare_Architecture_GB.Homework2'))


