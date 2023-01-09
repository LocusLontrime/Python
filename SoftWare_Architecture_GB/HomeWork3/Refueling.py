from abc import ABC, abstractmethod

class Refueling(ABC):

    @ abstractmethod
    def fuel(self, fuel_volume: int) -> None:
        ...


