import ItemGenerator
import StoneReward

class StoneGenerator(ItemGenerator.ItemGenerator):
    def create_item(self, l_border, r_border):
        # print(f'create_item from ItemGenerator call')
        return StoneReward.StoneReward(l_border, r_border)