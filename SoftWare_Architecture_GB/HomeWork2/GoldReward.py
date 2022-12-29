import random
import GameItem

class GoldReward(GameItem.GameItem):

    def open_item(self):
        # amount of gold obtainable from chest:
        random_amount = random.randrange(self.lb, self.rb + 1)
        print(f'{random_amount} gold obtained!!!')



