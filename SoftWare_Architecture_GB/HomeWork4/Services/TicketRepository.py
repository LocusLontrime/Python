from datetime import datetime

from AmberCode.SoftWare_Architecture_GB.HomeWork4.Models.Ticket import Ticket
from AmberCode.SoftWare_Architecture_GB.HomeWork4.Interfaces.ITicketRepo import ITicketRepo


class TicketRepository:
    __ticketRepository = None

    def __init__(self):
        self.__tickets = []
        date = datetime(2022, 10, 27)
        self.generate_tickets(1, 4, 10, date)
        self.generate_tickets(2, 4, 15, date)

    @ staticmethod
    def get_ticket_repository() -> 'TicketRepository':
        if TicketRepository.__ticketRepository is None:
            TicketRepository.__ticketRepository = TicketRepository()
        return TicketRepository.__ticketRepository

    def create(self, ticket: Ticket) -> bool:
        self.__tickets.append(ticket)
        return True

    def read_all(self, route_number: int) -> list[Ticket]:
        route_tickets = []
        for ticket in self.__tickets:
            if ticket.get_route_number() == route_tickets and ticket.get_valid():
                route_tickets.append(ticket)
        if not route_number:
            raise Exception(f'There are no tickets for this bus.')
        return route_tickets  # LOGIC ERROR in initial project!!!

    def update(self, ticket: Ticket) -> bool:
        for ticket_ in self.__tickets:
            if ticket_ == ticket:
                self.__tickets.remove(ticket_)
                self.__tickets.append(ticket)
                return True
        return False

    def delete(self, ticket: Ticket) -> bool:
        if ticket in self.__tickets:
            self.__tickets.remove(ticket)
            return True
        return False

    def generate_tickets(self, route_number: int, count_places: int, price: int, date: datetime):
        for i in range(1, count_places + 1):
            self.__tickets.append(Ticket(route_number, i, price, date, True))

