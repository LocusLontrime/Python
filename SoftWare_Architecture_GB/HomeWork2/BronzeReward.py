import random
import GameItem


class BronzeReward(GameItem.GameItem):
    def open_item(self):
        # amount of bronze obtainable from chest:
        random_amount = random.randrange(self.lb, self.rb + 1)
        print(f'{random_amount} bronze obtained!!!')