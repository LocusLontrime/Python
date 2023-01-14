from datetime import datetime
from EnterData import EnterData
from Aunthefication import Authentication
from AmberCode.SoftWare_Architecture_GB.HomeWork4.Core.Customer import Customer


# the main class of client application:
class Start(EnterData):
    # connection to the main logic is implemented through Customer "interface"

    def __init__(self):
        self.customer = None
        self.ticket_route_number = None
        self.ticket_date = None

    def run_login_register_menu(self) -> None:
        run = True
        while run:
            self.__print_message_line("Application for buying bus tickets")
            self.__print_message_line("This is a test version. The data base is not available in full mode.")
            self.__print_message_line("To login\t\t\tenter 1\nTo register\t\t\tenter 2\nTo exit\t\t\t\tenter 0")
            print("Enter your choice > ")
            try:
                choice = self._input_int(0, 2)
            except RuntimeError as e:
                print(f'error: {e}')
                continue
            print("=====================================================================================")
            run = self.run_login_register_menu_choice_logic(choice)

    def run_login_register_menu_choice_logic(self, choice: int) -> bool:
        match choice:
            case 1:
                self.__login()
                if self.customer.get_user() is not None:
                    self.__run_buying_menu()
            case 2:
                self.__register()
                if self.customer is not None:
                    self.__run_buying_menu()
            case _:
                return False
        return True

    def __login(self) -> None:
        self.__print_message_line("This is a test version. The data base is not available in full mode.")
        self.__print_message_line("Login")
        print("User name: ")
        user_name = self._input_str()
        print("Password: ")
        password_hash = hash(self._input_str())
        print("=====================================================================================")
        print("Enter the system... ")
        customer = Customer()
        try:
            self.customer.set_user(Authentication.authentication(self.customer.get_user_provider(), user_name, password_hash))
        except RuntimeError as e:
            print("FAIL")
            print(e)
            print("=====================================================================================")
            return
        self.__print_message_line("OK")

    def __register(self) -> None:
        self.__print_message_line("This is a test version. The data base is not available in full mode.")
        self.__print_message_line("Register")
        print("Enter user name: ")
        user_name = self._input_str()
        print("Enter password: ")
        password_hash = hash(self._input_str())
        print("Repeat password: ")
        password_hash2 = hash(self._input_str())
        if password_hash != password_hash2:
            print("=====================================================================================")
            self.__print_message_line("Passwords do not match. Exit register.")
            return
        print("Enter card number: ")
        card_number = self._input_int(1, 9999999999999999)
        print("=====================================================================================")
        print("Register the system... ")
        customer = Customer()
        id_: int
        try:
            id_ = self.customer.get_user_provider().create_client(user_name, password_hash, card_number)
            self.customer.set_user(Authentication.authentication(self.customer.get_user_provider(), user_name, password_hash))
        except RuntimeError as e:
            print("FAIL")
            print(e)
            print("=====================================================================================")
            return
        self.__print_message_line(
            "OK. user " + self.customer.get_user().get_user_name() + " with ID " + str(id_) + "added to base.")

    def __run_buying_menu(self) -> None:
        run = True
        while run:
            self.__print_message_line(
                "Application for buying bus tickets. | User " + self.customer.get_user().get_user_name() + " |")
            self.__print_message_line(
                "To select route number and print all tickets\tenter 1\nTo logout\t\t\t\t\t\t\t\t\t\tenter 0")
            print("Enter your choice > ")
            try:
                choice = self._input_int(0, 1)
            except RuntimeError as e:
                print("=====================================================================================")
                self.__print_message_line(str(e))
                continue
            print("=====================================================================================")
            run = self.__run_buying_menu_choice_logic(choice)

    def __run_buying_menu_choice_logic(self, choice: int) -> bool:
        match choice:
            case 1:
                self.ticket_route_number = self.__run_select_route_menu()
                if self.ticket_route_number > 0:
                    ticket_date = self.__run_select_date()
                    if ticket_date is not None:
                        try:
                            self.customer.set_selected_tickets(
                                self.customer.search_ticket(ticket_date, self.ticket_route_number))
                        except RuntimeError as e:
                            self.__print_message_line(str(e))
                            return True
                        self.__print_all_tickets(self.customer.get_selected_sickets())
                        self.__buy_ticket_menu()
                        return True
                    return True
                return True
            case _:
                return False

    def __run_select_route_menu(self) -> int:
        self.__print_message_line(
            "Input route number and date. | User " + self.customer.get_user().get_user_name() + " |")
        print("Route number > ")
        try:
            num_route = self._input_int(1, 2)
        except RuntimeError as e:
            self.__print_message_line(str(e))
            return -1
        print("=====================================================================================")
        return num_route

    def __run_select_date(self) -> datetime or None:
        print("Date (format: YYYY-MM-DD) > ")

        try:
            date = self._input_date()
        except RuntimeError as e:
            self.__print_message_line(str(e))
            return None
        print("=====================================================================================")
        return date

    def __print_all_tickets(self, ticks) -> None:
        for t in ticks:
            print(str(t))
        print("=====================================================================================")

    def __buy_ticket_menu(self) -> None:
        self.__print_message_line("Confirm to buy. | User " + self.customer.get_user().get_userName() + " |")
        print(
            "To buy a ticket for bus route " + self.ticket_route_number + " on the " + self.ticket_date + " enter" + " \"Yes\" > ")
        answer = self._input_str()
        print("=====================================================================================")
        self.__buy_ticket_menu_confirm_logic(answer)

    def __buy_ticket_menu_confirm_logic(self, answer: str) -> None:
        if answer.lower() == "YES".lower():
            for t in self.customer.getSelectedTickets():
                if t.get_date().equals(self.ticket_date) and t.get_route_number() == self.ticket_route_number and t.get_valid():
                    try:
                        flag = self.customer.buy_ticket(t)
                    except RuntimeError as e:
                        self.__print_message_line(str(e))
                        return
                    if flag:
                        self.__print_message_line(t.to_print())
                        return

    def __print_message_line(self, message: str) -> None:
        print(message)
        print("=====================================================================================")

