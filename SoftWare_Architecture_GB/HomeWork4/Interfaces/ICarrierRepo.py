from abc import ABC, abstractmethod
from AmberCode.SoftWare_Architecture_GB.HomeWork4.Models.Carrier import Carrier


class ICarrierRepo(ABC):
    @abstractmethod
    def read(self, id_) -> Carrier:
        ...


