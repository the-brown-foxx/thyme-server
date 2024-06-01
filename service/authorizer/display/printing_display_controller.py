from service.authorizer.display.display_controller import DisplayController
from service.registry.model.car import Car


class PrintingDisplayController(DisplayController):
    def show_instructions(self):
        print('Please pull up in front of the gate')

    def show_car_info(self, car: Car):
        print(f'Welcome, {car.color} {car.year} {car.make} {car.model} [{car.registration_id}]!')

    def show_unauthorized_message(self, registration_id: str):
        print(f'Thou shall not pass, {registration_id}')

    def update_vacant_space(self, vacant_space: int):
        print(f'Updated vacant space to {vacant_space}')
