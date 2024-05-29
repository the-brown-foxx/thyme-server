from asyncio import create_task

from service.authorizer.display.display_controller import DisplayController
from service.connection.connection_manager import ConnectionManager
from service.registry.model.car import Car


class ConnectedDisplayController(DisplayController):
    connection_manager: ConnectionManager

    def __init__(self, connection_manager: ConnectionManager):
        self.connection_manager = connection_manager
        create_task(connection_manager.connect())

    def show_instructions(self):
        create_task(self.connection_manager.send_message({'status': 'SHOW_INSTRUCTION'}))

    def show_car_info(self, car: Car):
        create_task(
            self.connection_manager.send_message({
                'status': 'CAR_AUTHORIZED',
                'car': car,
            })
        )

    def show_unauthorized_message(self, registration_id: str):
        create_task(
            self.connection_manager.send_message({
                'status': 'CAR_UNAUTHORIZED',
                'registration_id': registration_id,
            })
        )
