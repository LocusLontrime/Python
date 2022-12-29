import ItemGenerator
import IronReward

class IronGenerator(ItemGenerator.ItemGenerator):
    def create_item(self, l_border, r_border):
        # print(f'create_item from ItemGenerator call')
        return IronReward.IronReward(l_border, r_border)