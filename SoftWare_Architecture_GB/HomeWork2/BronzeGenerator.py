import ItemGenerator
import BronzeReward

class BronzeGenerator(ItemGenerator.ItemGenerator):
    def create_item(self, l_border, r_border):
        # print(f'create_item from ItemGenerator call')
        return BronzeReward.BronzeReward(l_border, r_border)