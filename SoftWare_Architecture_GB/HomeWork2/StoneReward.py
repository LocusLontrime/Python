import random
import GameItem

class StoneReward(GameItem.GameItem):
    def open_item(self):
        # amount of stone obtainable from chest:
        random_amount = random.randrange(self.lb, self.rb + 1)
        print(f'{random_amount} stone obtained!!!')