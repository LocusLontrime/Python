from CashProvider import CashProvider
from TicketProvider import TicketProvider
from UserProvider import UserProvider
from AmberCode.SoftWare_Architecture_GB.HomeWork4.Interfaces.ICustomer import ICustomer


class Customer(ICustomer):
    def __init__(self):
        self.__ticket_provider = TicketProvider()
        self.__cash_provider = CashProvider()
        self.__user_provider = UserProvider()
        self.__client = None
        self.__tickets_selected = []

    def get_tickets_selected(self):
        return self.__tickets_selected

    def set_tickets_selected(self, tickets_selected):
        self.__tickets_selected = tickets_selected

    def get_user_provider(self):
        return self.__user_provider

    def get_user(self):
        return self.__client

    def set_user(self, client):
        self.__client = client

    def buy_ticket(self, ticket):
        self.__cash_provider.authorization(self.__client)
        flag = self.__cash_provider.buy(ticket)
        if flag:
            flag = self.__ticket_provider.update_ticket_status(ticket)
        return flag

    def search_ticket(self, date, route):
        result = []
        list_ = self.__ticket_provider.get_tickets(route)
        for ticket in list_:
            if ticket.get_date() == date:
                result.append(ticket)
        if not result:
            raise RuntimeError(f'There are no tickets for this date')
        return result




