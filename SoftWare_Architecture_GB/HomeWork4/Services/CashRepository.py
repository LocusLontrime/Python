import random

import numpy

from AmberCode.SoftWare_Architecture_GB.HomeWork4.Models.BankAccount import BankAccount
from AmberCode.SoftWare_Architecture_GB.HomeWork4.Interfaces.ICashRepo import ICashRepo


class CashRepository:

    __cash_repository = None

    def __init__(self):
        self.__clients = []
        for i in range(1, 6):
            # old good bank random cards -->>
            self.__clients.append(BankAccount(random.randrange(10 ** 16, 10 ** 17 - 1)))

    def get_clients(self) -> list[BankAccount]:
        return self.__clients

    @staticmethod
    def get_cash_repository() -> 'CashRepository':
        if CashRepository.__cash_repository is None:
            CashRepository.__cash_repository = CashRepository()
        return CashRepository.__cash_repository

    def transaction(self, payment: int, card_form: int, carrier_card: int) -> bool:
        from_, to_ = None, None
        for client in self.__clients:
            if client.get_card() == card_form:
                from_ = client
            if client.get_card() == carrier_card:
                to_ = client
        if from_ is None:
            raise Exception(f'"No withdrawal account."')
        if to_ is None:
            raise Exception(f'No money account.')

        if from_.get_balance() - payment < 0:
            raise Exception(f'Insufficient funds.')
        if to_.get_balance() > numpy.Infinity - payment:  # Levi Gin (Evgeniy Cherkasov) idea
            raise Exception(f'Too much amount.')

        try:
            ...
        finally:
            self.__clients.remove(from_)
            self.__clients.remove(to_)
            from_.set_balance(from_.get_balance() - payment)
            to_.set_balance(to_.get_balance() + payment)
            self.__clients.append(from_)
            self.__clients.append(to_)

        return True


