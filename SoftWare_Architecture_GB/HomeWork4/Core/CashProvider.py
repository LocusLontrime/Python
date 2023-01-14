from AmberCode.SoftWare_Architecture_GB.HomeWork4.Services.CashRepository import CashRepository
from AmberCode.SoftWare_Architecture_GB.HomeWork4.Services.CarrierRepository import CarrierRepository


class CashProvider:
    def __init__(self):
        self.carrier_repository = CarrierRepository.getCarrierRepository()
        self.cash_repository = CashRepository.getCashRepository()

    def buy(self, ticket):
        ...

    def authorization(self, client):
        ...

