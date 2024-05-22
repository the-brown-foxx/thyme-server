from typing import Union

from service.authenticator.log.car_logger import CarLogger
from service.authorizer.access.parking_access_control import ParkingAccessControl
from service.authorizer.display.display_controller import DisplayController
from service.authorizer.gate.gate_controller import GateController
from service.authorizer.monitor.car.car_monitor import CarMonitor
from service.registry.car_registry import CarRegistry
from service.registry.model.car import Car


class ActualParkingAccessControl(ParkingAccessControl):
    car_monitor: CarMonitor
    gate_controller: GateController
    display_controller: DisplayController
    car_logger: CarLogger

    def __init__(
            self,
            car_monitor: CarMonitor,
            gate_controller: GateController,
            display_controller: DisplayController,
            car_logger: CarLogger,
    ):
        self.car_monitor = car_monitor
        self.gate_controller = gate_controller
        self.display_controller = display_controller
        self.car_logger = car_logger

    def on_car_detected(self, car_or_registration_id: Union[Car, str]):
        if isinstance(car_or_registration_id, Car):
            car = car_or_registration_id
            self.gate_controller.open_gate()
            self.display_controller.show_car_info(car)
            self.car_logger.log(car_registration_id=car.registration_id, entering=True)
        elif isinstance(car_or_registration_id, str):
            registration_id = car_or_registration_id
            self.display_controller.show_unauthorized_message(registration_id)

    def start(self):
        (self.car_monitor.get_car_stream()
         .subscribe(lambda registration_id: self.on_car_detected(registration_id)))

    def stop(self):
        pass
