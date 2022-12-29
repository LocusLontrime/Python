from abc import ABC, abstractmethod
# interface -->>
class GameItem(ABC):
    def __init__(self, l_border: int, r_border: int):
        self.lb, self.rb = l_border, r_border

    @abstractmethod
    def open_item(self):
        pass


