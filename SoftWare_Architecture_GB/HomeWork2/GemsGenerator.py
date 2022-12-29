import ItemGenerator
import GemsReward
class GemsGenerator(ItemGenerator.ItemGenerator):
    def create_item(self, l_border, r_border):
        # print(f'create_item from ItemGenerator call')
        return GemsReward.GemsReward(l_border, r_border)