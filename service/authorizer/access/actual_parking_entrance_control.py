from service.authorizer.access.parking_access_control import ParkingAccessControl
from service.authorizer.display.display_controller import DisplayController
from service.authorizer.gate.gate_controller import GateController
from service.authorizer.log.car_logger import CarLogger
from service.authorizer.monitor.car.car_monitor import CarMonitor
from service.authorizer.monitor.model.car_snapshot import CarSnapshot
from service.authorizer.parking.parking_space_counter import ParkingSpaceCounter
from service.exception import UnsetParkingSpaceError
from service.registry.model.car import Car


class ActualParkingAccessControl(ParkingAccessControl):
    def __init__(
            self,
            car_monitor: CarMonitor,
            gate_controller: GateController,
            display_controller: DisplayController,
            parking_space_counter: ParkingSpaceCounter,
            car_logger: CarLogger,
            entrance: bool,
    ):
        self.car_monitor = car_monitor
        self.gate_controller = gate_controller
        self.display_controller = display_controller
        self.parking_space_counter = parking_space_counter
        self.car_logger = car_logger
        self.entrance = entrance
        self._start()

    def _start(self):
        (self.car_monitor.get_car_stream()
         .subscribe(lambda car_snapshot: self._on_car_detected(car_snapshot)))

        try:
            vacant_space = self.parking_space_counter.get_parking_space_count().vacant_space
            self.display_controller.update_vacant_space(vacant_space)

        except UnsetParkingSpaceError:
            pass

    def _on_car_detected(self, car_snapshot: CarSnapshot):
        if car_snapshot.car is not None:

            if self.entrance:
                self.parking_space_counter.decrement_available_space()
            else:
                self.parking_space_counter.increment_available_space()

            self.display_controller.show_car_info(car_snapshot.car)
            vacant_space = self.parking_space_counter.get_parking_space_count().vacant_space
            self.display_controller.update_vacant_space(vacant_space)
            self.car_logger.log(car_snapshot, entering=self.entrance)

            vehicle_passed = self.gate_controller.open_gate()
            vehicle_passed.subscribe(on_next=lambda passed: self._vehicle_passed_on_next(passed))

        else:
            self.display_controller.show_unauthorized_message(car_snapshot.registration_id)

    def _vehicle_passed_on_next(self, passed: bool):
        if passed:
            self.car_monitor.mark_car_as_passed()
            self.display_controller.show_instructions()
