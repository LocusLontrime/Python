import GameItem
from abc import ABC, abstractmethod
# abstract class -->>
class ItemGenerator(ABC):
    def __init__(self, l_border, r_border):
        self.lb, self.rb = l_border, r_border


    @abstractmethod
    def create_item(self, l_border, r_border) -> 'GameItem.GameItem':
        pass

    def open_reward(self):
        game_item = self.create_item(self.lb, self.rb)
        game_item.open_item()



