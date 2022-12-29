import ItemGenerator
import PlatinumReward

class PlatinumGenerator(ItemGenerator.ItemGenerator):
    def create_item(self, l_border, r_border):
        # print(f'create_item from ItemGenerator call')
        return PlatinumReward.PlatinumReward(l_border, r_border)