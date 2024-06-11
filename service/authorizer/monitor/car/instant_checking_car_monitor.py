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
    car_passed: bool
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
        self.car_passed = True
        self.car_stream = Subject()
        (license_plate_monitor.get_registration_id_stream()
         .subscribe(lambda registration_id: self.on_next(registration_id)))

    def on_next(self, registration_id: str):
        registration_id = self.registration_id_format.preformat(registration_id)
        print(registration_id)
        if not self.registration_id_format.valid(registration_id):
            return

        try:
            car = self.car_registry.get_car(registration_id)

            if self.car_passed:
                self.car_stream.on_next(car)
                self.car_passed = False

        except CarNotFoundError:
            new_score = self.failure_scores.get(registration_id, 0) + 1
            self.failure_scores[registration_id] = new_score

            if self.failure_scores[registration_id] >= self.failing_score:
                self.failure_scores = {}
                self.car_stream.on_next(registration_id)

    def get_car_stream(self) -> Observable[Union[Car, str]]:
        return self.car_stream

    def mark_car_as_passed(self):
        self.car_passed = True

