from typing import Callable

from service.authorizer.display.display_controller import DisplayController
from service.registry.model.car import Car


class PrintingDisplayController(DisplayController):
    def __init__(self, on_vacant_space_change: Callable[[int], None], entrance: bool):
        self.on_vacant_space_change = on_vacant_space_change
        self.entrance = entrance

    def show_instructions(self):
        print('Please pull up in front of the gate')

    def show_parking_full(self):
        print('Parking space is full!')

    def show_car_info(self, car: Car):
        greeting = 'Welcome' if self.entrance else "Bye bye"
        print(f'{greeting}, {car.color} {car.year} {car.make} {car.model} [{car.registration_id}]!')

    def show_unauthorized_message(self, registration_id: str):
        print(f'Thou shall not pass, {registration_id}')

    def update_vacant_space(self, vacant_space: int):
        print(f'Updated vacant space to {vacant_space}')
        self.on_vacant_space_change(vacant_space)
