import serial
import time
import threading
from queue import Queue, Empty
from typing import Union
from service.authorizer.access.parking_access_control import ParkingAccessControl
from service.authorizer.display.display_controller import DisplayController
from service.authorizer.gate.gate_controller import GateController
from service.authorizer.log.car_logger import CarLogger
from service.authorizer.monitor.car.car_monitor import CarMonitor
from service.authorizer.parking.parking_space_counter import ParkingSpaceCounter
from service.registry.model.car import Car


class ParkingEntranceControl(ParkingAccessControl):
    car_monitor: CarMonitor
    gate_controller: GateController
    display_controller: DisplayController
    parking_space_counter: ParkingSpaceCounter
    car_logger: CarLogger

    def __init__(
            self,
            car_monitor: CarMonitor,
            gate_controller: GateController,
            display_controller: DisplayController,
            parking_space_counter: ParkingSpaceCounter,
            car_logger: CarLogger,
    ):
        self.car_monitor = car_monitor
        self.gate_controller = gate_controller
        self.display_controller = display_controller
        self.parking_space_counter = parking_space_counter
        self.car_logger = car_logger

    def on_car_detected(self, car_or_registration_id: Union[Car, str]):
        if isinstance(car_or_registration_id, Car):
            car = car_or_registration_id
            self.parking_space_counter.decrement_available_space()
            self.display_controller.show_car_info(car)
            vacant_space = self.parking_space_counter.get_parking_space_count().vacant_space
            self.display_controller.update_vacant_space(vacant_space)
            self.car_logger.log(car_registration_id=car.registration_id, entering=True)

            vehicle_passed = self.gate_controller.open_gate()
            vehicle_passed.subscribe(on_next=lambda passed: self.vehicle_passed_on_next(passed))

        elif isinstance(car_or_registration_id, str):
            registration_id = car_or_registration_id
            self.display_controller.show_unauthorized_message(registration_id)

    def vehicle_passed_on_next(self, passed: bool):
        if passed:
            self.car_monitor.mark_car_as_passed()

    def start(self):
        (self.car_monitor.get_car_stream()
         .subscribe(lambda registration_id: self.on_car_detected(registration_id)))
        vacant_space = self.parking_space_counter.get_parking_space_count().vacant_space
        self.display_controller.update_vacant_space(vacant_space)

    def stop(self):
        pass
