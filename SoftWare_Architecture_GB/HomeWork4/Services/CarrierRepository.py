from AmberCode.SoftWare_Architecture_GB.HomeWork4.Interfaces.ICarrierRepo import ICarrierRepo
from AmberCode.SoftWare_Architecture_GB.HomeWork4.Models.Carrier import Carrier


class CarrierRepository(ICarrierRepo):

    __carrier_repository = None

    def __init__(self):
        self.__carriers = [Carrier(1, 1)]

    @staticmethod
    def get_carrier_repository() -> 'CarrierRepository':
        if CarrierRepository.__carrier_repository is None:
            CarrierRepository.__carrier_repository = CarrierRepository()
        return CarrierRepository.__carrier_repository

    def read(self, id_: int) -> Carrier:
        for carrier in self.__carriers:
            if carrier.get_id() == id_:
                return carrier
        raise Exception(f'A carrier with this ID not found')

