from typing import Union, Optional

from reactivex import Observable, Subject

from service.authorizer.format.registration_id_format import RegistrationIdFormat
from service.authorizer.monitor.car.car_monitor import CarMonitor
from service.authorizer.monitor.license.license_plate_monitor import LicensePlateMonitor
from service.exception import CarNotFoundError
from service.registry.car_registry import CarRegistry
from service.registry.model.car import Car


class InstantCheckingCarMonitor(CarMonitor):
    failing_score = 20  # TODO: This could be raised in actual, because the car will stop in front of the gate
    car_registry: CarRegistry
    registration_id_format: RegistrationIdFormat
    last_registration_id: Optional[str]
    failure_scores: dict[str, int]
    car_stream: Subject[Union[Car, str]]

    def __init__(
            self,
            license_plate_monitor: LicensePlateMonitor,
            car_registry: CarRegistry,
            registration_id_format: RegistrationIdFormat
    ):
        self.car_registry = car_registry
        self.registration_id_format = registration_id_format
        self.failure_scores = {}
        self.last_registration_id = None
        self.car_stream = Subject()
        (license_plate_monitor.get_registration_id_stream()
         .subscribe(lambda registration_id: self.on_next(registration_id)))

    def on_next(self, registration_id: str):
        registration_id = self.registration_id_format.preformat(registration_id)
        if not self.registration_id_format.valid(registration_id):
            return

        try:
            car = self.car_registry.get_car(registration_id)

            if self.last_registration_id is None or registration_id not in self.last_registration_id:
                self.car_stream.on_next(car)
                self.last_registration_id = registration_id
        except CarNotFoundError:
            new_score = self.failure_scores.get(registration_id, 0) + 1
            self.failure_scores[registration_id] = new_score

            if self.failure_scores[registration_id] >= self.failing_score:
                self.failure_scores = {}

                if self.last_registration_id is None or registration_id not in self.last_registration_id:
                    self.car_stream.on_next(registration_id)
                    self.last_registration_id = registration_id

    def get_car_stream(self) -> Observable[Union[Car, str]]:
        return self.car_stream

    def mark_car_as_passed(self):
        self.last_registration_id = None

