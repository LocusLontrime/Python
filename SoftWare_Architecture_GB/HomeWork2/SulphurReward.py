import random
import GameItem

class SulphurReward(GameItem.GameItem):
    def open_item(self):
        # amount of sulphur obtainable from chest:
        random_amount = random.randrange(self.lb, self.rb + 1)
        print(f'{random_amount} sulphur obtained!!!')