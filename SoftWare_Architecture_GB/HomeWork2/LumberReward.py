import random
import GameItem

class LumberReward(GameItem.GameItem):
    def open_item(self):
        # amount of lumber obtainable from chest:
        random_amount = random.randrange(self.lb, self.rb + 1)
        print(f'{random_amount} lumber obtained!!!')