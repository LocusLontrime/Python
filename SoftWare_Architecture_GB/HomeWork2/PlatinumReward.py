import random
import GameItem

class PlatinumReward(GameItem.GameItem):
    def open_item(self):
        # amount of platinum obtainable from chest:
        random_amount = random.randrange(self.lb, self.rb + 1)
        print(f'{random_amount} platinum obtained!!!')