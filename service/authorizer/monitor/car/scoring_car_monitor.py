from typing import Union

from reactivex import Observable, Subject

from service.authorizer.filter.scoring_registration_id_filter import ScoringRegistrationIdFilter
from service.authorizer.format.registration_id_format import RegistrationIdFormat
from service.authorizer.monitor.car.car_monitor import CarMonitor
from service.authorizer.monitor.license.license_plate_monitor import LicensePlateMonitor
from service.exception import CarNotFoundError
from service.registry.car_registry import CarRegistry
from service.registry.model.car import Car


class ScoringCarMonitor(CarMonitor):
    car_registry: CarRegistry
    car_stream: Subject[Union[Car, str]]

    def __init__(
            self,
            license_plate_monitor: LicensePlateMonitor,
            car_registry: CarRegistry,
            registration_id_format: RegistrationIdFormat,
    ):
        self.car_registry = car_registry
        self.car_stream = Subject()
        scoring_registration_id_filter = ScoringRegistrationIdFilter(registration_id_format)
        filtered_license_plate_stream = (scoring_registration_id_filter
                                         .get_filtered_stream(license_plate_monitor.get_registration_id_stream()))
        filtered_license_plate_stream.subscribe(
            on_next=lambda registration_id: self.on_next(registration_id))

    def on_next(self, registration_id: str):
        try:
            self.car_stream.on_next(self.car_registry.get_car(registration_id))
        except CarNotFoundError:
            self.car_stream.on_next(registration_id)

    def get_car_stream(self) -> Observable[Car]:
        return self.car_stream

    def mark_car_as_passed(self):
        pass
