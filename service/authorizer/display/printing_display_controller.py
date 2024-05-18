from service.authorizer.display.display_controller import DisplayController
from service.registry.model.car import Car


class PrintingDisplayController(DisplayController):
    def show_instructions(self):
        print('Please pull up in front of the gate')

    def show_car_info(self, car: Car):
        print(f'Welcome, {car.color} {car.year} {car.make} {car.model} [{car.registration_id}]!')

    def show_unauthorized_message(self):
        print('Thou shall not pass!')
