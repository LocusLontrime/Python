import random
import GameItem

class SilverReward(GameItem.GameItem):
    def open_item(self):
        # amount of silver obtainable from chest:
        random_amount = random.randrange(self.lb, self.rb + 1)
        print(f'{random_amount} silver obtained!!!')