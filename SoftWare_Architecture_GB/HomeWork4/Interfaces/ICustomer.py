from abc import ABC, abstractmethod
from AmberCode.SoftWare_Architecture_GB.HomeWork4.Models.Ticket import Ticket
from AmberCode.SoftWare_Architecture_GB.HomeWork4.Models.User import User
from AmberCode.SoftWare_Architecture_GB.HomeWork4.Core.UserProvider import UserProvider


class ICustomer(ABC):

    def get_tickets_selected(self) -> list[Ticket]:
        ...

    def set_tickets_selected(self, tickets_selected) -> None:
        ...

    def get_user(self) -> User:
        ...

    def set_user(self, client) -> None:
        ...

    def get_user_provider(self) -> UserProvider:
        ...

    def buy_ticket(self, ticket) -> bool:
        ...

    def search_ticket(self, data, route) -> list[Ticket]:
        ...





