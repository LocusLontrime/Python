from AmberCode.SoftWare_Architecture_GB.HomeWork4.Core.UserProvider import UserProvider
from AmberCode.SoftWare_Architecture_GB.HomeWork4.Services.CashRepository import CashRepository
from AmberCode.SoftWare_Architecture_GB.HomeWork4.Services.CarrierRepository import CarrierRepository
from AmberCode.SoftWare_Architecture_GB.HomeWork4.Models.User import User
from AmberCode.SoftWare_Architecture_GB.HomeWork4.ClientApplication.Aunthefication import Authentication


class CashProvider:
    def __init__(self, card_number):
        self.card_number = card_number
        self.is_authorized = False
        self.carrier_repository = CarrierRepository.get_carrier_repository()
        self.cash_repository = CashRepository.get_cash_repository()

    def buy(self, ticket):
        carrier = self.carrier_repository.read(1)
        return self.cash_repository.transaction(ticket.getPrice(), self.card_number, carrier.get_card_number())

    def authorization(self, client: User):
        self.is_authorized = Authentication.authentication(UserProvider(), client.get_user_name(), client.get_hash_password())

