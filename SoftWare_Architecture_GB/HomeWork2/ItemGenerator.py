import GameItem
# abstract class -->>
class ItemGenerator:
    def __init__(self, l_border, r_border):
        self.lb, self.rb = l_border, r_border


    # abstract method
    def create_item(self, l_border, r_border) -> 'GameItem.GameItem':
        pass

    def open_reward(self):
        game_item = self.create_item(self.lb, self.rb)
        game_item.open_item()