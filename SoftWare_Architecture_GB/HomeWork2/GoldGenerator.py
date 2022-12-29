import ItemGenerator
import GoldReward
class GoldGenerator(ItemGenerator.ItemGenerator):
    def create_item(self, l_border, r_border):
        # print(f'create_item from GoldGenerator call')
        return GoldReward.GoldReward(l_border, r_border)