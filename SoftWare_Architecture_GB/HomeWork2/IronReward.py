import random
import GameItem

class IronReward(GameItem.GameItem):
    def open_item(self):
        # amount of iron obtainable from chest:
        random_amount = random.randrange(self.lb, self.rb + 1)
        print(f'{random_amount} iron obtained!!!')