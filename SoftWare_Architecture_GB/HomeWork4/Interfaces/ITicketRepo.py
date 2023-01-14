from abc import ABC, abstractmethod
from AmberCode.SoftWare_Architecture_GB.HomeWork4.Models.Ticket import Ticket


class ITicketRepo(ABC):
    @abstractmethod
    def create(self, ticket: 'Ticket') -> bool:
        ...

    @abstractmethod
    def read_all(self, route_number: int) -> list[Ticket]:
        ...

    @abstractmethod
    def update(self, ticket) -> bool:
        ...

    @abstractmethod
    def delete(self, ticket) -> bool:
        ...

