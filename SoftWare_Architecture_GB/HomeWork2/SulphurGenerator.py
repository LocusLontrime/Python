import ItemGenerator
import SulphurReward

class SulphurGenerator(ItemGenerator.ItemGenerator):
    def create_item(self, l_border, r_border):
        # print(f'create_item from ItemGenerator call')
        return SulphurReward.SulphurReward(l_border, r_border)