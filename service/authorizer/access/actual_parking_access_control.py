from service.authenticator.log.car_logger import CarLogger
from service.authorizer.access.parking_access_control import ParkingAccessControl
from service.authorizer.display.display_controller import DisplayController
from service.authorizer.gate.gate_controller import GateController
from service.authorizer.monitor.license_plate_monitor import LicensePlateMonitor
from service.exception import CarNotFoundError
from service.registry.car_registry import CarRegistry


class ActualParkingAccessControl(ParkingAccessControl):
    license_plate_monitor: LicensePlateMonitor
    car_registry: CarRegistry
    gate_controller: GateController
    display_controller: DisplayController
    car_logger: CarLogger

    def __init__(
            self,
            license_plate_monitor: LicensePlateMonitor,
            car_authorizer: CarRegistry,
            gate_controller: GateController,
            display_controller: DisplayController,
            car_logger: CarLogger,
    ):
        self.license_plate_monitor = license_plate_monitor
        self.car_registry = car_authorizer
        self.gate_controller = gate_controller
        self.display_controller = display_controller
        self.car_logger = car_logger

    def on_license_plate_detected(self, registration_id: str):
        try:
            car = self.car_registry.get_car(registration_id)
            entering = True
            self.gate_controller.open_gate()
            self.display_controller.show_car_info(car)
            self.car_logger.log(registration_id, entering)
        except CarNotFoundError:
            self.display_controller.show_unauthorized_message(registration_id)

    def start(self):
        (self.license_plate_monitor.get_registration_id_stream()
         .subscribe(lambda registration_id: self.on_license_plate_detected(registration_id)))

    def stop(self):
        pass
