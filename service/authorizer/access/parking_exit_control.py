from typing import Union

from service.authorizer.access.parking_access_control import ParkingAccessControl
from service.authorizer.display.display_controller import DisplayController
from service.authorizer.gate.gate_controller import GateController
from service.authorizer.log.car_logger import CarLogger
from service.authorizer.monitor.car.car_monitor import CarMonitor
from service.registry.model.car import Car


class ParkingExitControl(ParkingAccessControl):
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
        self.gate_controller.open_gate()
        # TODO: Show goodbye or something
        if isinstance(car_or_registration_id, Car):
            car = car_or_registration_id
            self.car_logger.log(car_registration_id=car.registration_id, entering=False)
        elif isinstance(car_or_registration_id, str):
            registration_id = car_or_registration_id
            self.car_logger.log(car_registration_id=registration_id, entering=False)
        # TODO: call car_monitor.mark_car_as_passed() after the arduino has
        #  signaled that the car has passed successfully

    def start(self):
        (self.car_monitor.get_car_stream()
         .subscribe(lambda registration_id: self.on_car_detected(registration_id)))

    def stop(self):
        pass
