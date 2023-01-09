from Car import Car

class FutureCar(Car):
    def __init__(self):
        super().__init__()
        # self.wheels_quantity = 3 -->> it violates LS principe

    def move(self, position: str):
        pass

    def maintenance(self):
        pass

    def switch_gear(self, delta: int):
        pass

    def headlights_on(self):
        pass

    def wipers_on(self):
        pass

    def headlights_off(self):
        pass

    def wipers_off(self):
        pass

    def fly(self, position: str):  # LS principe is not violated, flies to the position chosen
        pass



