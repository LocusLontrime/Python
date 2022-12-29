import ItemGenerator
import LumberReward

class LumberGenerator(ItemGenerator.ItemGenerator):
    def create_item(self, l_border, r_border):
        # print(f'create_item from ItemGenerator call')
        return LumberReward.LumberReward(l_border, r_border)