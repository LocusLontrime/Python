from AmberCode.SoftWare_Architecture_GB.HomeWork4.Services.TicketRepository import TicketRepository


class TicketProvider:
    def __init__(self):
        self.ticket_repo = TicketRepository.get_ticket_repository()

    def get_tickets(self, route):
        ...

    def update_ticket_status(self, ticket):
        ...

