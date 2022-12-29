import random
import GameItem

class GemsReward(GameItem.GameItem):

    def open_item(self):
        # quantity of gems obtainable from chest:
        random_amount = random.randrange(self.lb, self.rb + 1)
        print(f'{random_amount} gems obtained!!!')