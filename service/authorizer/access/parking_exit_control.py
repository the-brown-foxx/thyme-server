# from typing import Union
#
# from service.authorizer.access.parking_access_control import ParkingAccessControl
# from service.authorizer.display.display_controller import DisplayController
# from service.authorizer.gate.gate_controller import GateController
# from service.authorizer.log.car_logger import CarLogger
# from service.authorizer.monitor.car.car_monitor import CarMonitor
# from service.authorizer.parking.parking_space_counter import ParkingSpaceCounter
# from service.registry.model.car import Car
#
#
# class ParkingExitControl(ParkingAccessControl):
#     car_monitor: CarMonitor
#     gate_controller: GateController
#     display_controller: DisplayController
#     parking_space_counter: ParkingSpaceCounter
#     car_logger: CarLogger
#
#     def __init__(
#             self,
#             car_monitor: CarMonitor,
#             gate_controller: GateController,
#             display_controller: DisplayController,
#             parking_space_counter: ParkingSpaceCounter,
#             car_logger: CarLogger,
#     ):
#         self.car_monitor = car_monitor
#         self.gate_controller = gate_controller
#         self.display_controller = display_controller
#         self.parking_space_counter = parking_space_counter
#         self.car_logger = car_logger
#         self._start()
#
#     def _on_car_detected(self, car_or_registration_id: Union[Car, str]):
#         self.parking_space_counter.increment_available_space()
#         vacant_space = self.parking_space_counter.get_parking_space_count().vacant_space
#         self.display_controller.update_vacant_space(vacant_space)
#
#         if isinstance(car_or_registration_id, Car):
#             car = car_or_registration_id
#             self.car_logger.log(car_registration_id=car.registration_id, entering=False)
#
#         elif isinstance(car_or_registration_id, str):
#             registration_id = car_or_registration_id
#             self.car_logger.log(car_registration_id=registration_id, entering=False)
#
#         vehicle_passed = self.gate_controller.open_gate()
#         vehicle_passed.subscribe(on_next=lambda passed: self._vehicle_passed_on_next(passed))
#
#     def _vehicle_passed_on_next(self, passed: bool):
#         if passed:
#             self.car_monitor.mark_car_as_passed()
#
#     def _start(self):
#         (self.car_monitor.get_car_stream()
#          .subscribe(lambda registration_id: self._on_car_detected(registration_id)))
