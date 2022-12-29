import ItemGenerator
import SilverReward

class SilverGenerator(ItemGenerator.ItemGenerator):
    def create_item(self, l_border, r_border):
        # print(f'create_item from ItemGenerator call')
        return SilverReward.SilverReward(l_border, r_border)