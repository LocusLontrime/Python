import random
import GameItem

class CopperReward(GameItem.GameItem):
    def open_item(self):
        # amount of copper obtainable from chest:
        random_amount = random.randrange(self.lb, self.rb + 1)
        print(f'{random_amount} copper obtained!!!')