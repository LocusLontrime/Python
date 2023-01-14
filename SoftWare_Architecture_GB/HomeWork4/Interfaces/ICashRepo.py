from abc import ABC, abstractmethod


class ICashRepo(ABC):
    @abstractmethod
    def transaction(self, payment, card_from, card_to) -> bool:
        ...





