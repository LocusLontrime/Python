from Car import Car
from Refueling import Refueling
from Wipe import Wipe

class LexusRX350(Car, Refueling, Wipe):

    def __init__(self, vin_num: str, is_fuel_gasoline: bool, is_gear_box_mt: bool, colour: tuple[int, int, int]):
        super().__init__()
        self.VIN = vin_num

        self.capacity = 5  # people

        self.make = 'Lexus'
        self.model = 'RX350'

        self.car_type = self.type_car_dict[3]
        self.fuel_type = self.type_fuel_dict[int(is_fuel_gasoline)]
        self.gear_box_type = self.type_gear_box_dict[int(is_gear_box_mt)]

        self.wheels_quantity = 4
        self.engine_volume = 3.5

        self.colour = colour

    def fuel(self, fuel_volume: int):  # DI principe is not for Python
        match self.fuel_type:
            case 'Gasoline':
                ...
            case 'Diesel':
                ...
            case 'Electricity':
                ...

    def wip_windshield(self):
        pass

    def wip_headlights(self):
        pass

    def wip_mirrors(self):
        pass

    def move(self, position: str):
        pass

    def maintenance(self):
        pass

    def switch_gear(self, delta: int):
        pass

    def headlights_on(self):
        pass

    def wipers_on(self):
        pass

    def headlights_off(self):
        pass

    def wipers_off(self):
        pass

    def climate_control_on(self):
        pass

    def climate_control_off(self):
        pass

    def audio_on(self):
        pass

    def audio_off(self):
        pass

    def set_volume(self, volume: int):
        pass


red_new_lexus_rx350 = LexusRX350('1B3ES66S13D202162', True, True, (255, 0, 0))

# SR principe is not violated
