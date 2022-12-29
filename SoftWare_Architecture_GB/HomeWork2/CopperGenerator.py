import ItemGenerator
import CopperReward

class CopperGenerator(ItemGenerator.ItemGenerator):
    def create_item(self, l_border, r_border):
        # print(f'create_item from ItemGenerator call')
        return CopperReward.CopperReward(l_border, r_border)