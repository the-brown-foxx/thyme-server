from dataclasses import replace

from reactivex import Observable, Subject

from service.authorizer.format.registration_id_format import RegistrationIdFormat
from service.authorizer.monitor.car.car_monitor import CarMonitor
from service.authorizer.monitor.license.license_plate_monitor import LicensePlateMonitor
from service.authorizer.monitor.model.car_snapshot import CarSnapshot
from service.exception import CarNotFoundError
from service.registry.car_registry import CarRegistry


class InstantCheckingCarMonitor(CarMonitor):
    failing_score = 20

    def __init__(
            self,
            license_plate_monitor: LicensePlateMonitor,
            car_registry: CarRegistry,
            registration_id_format: RegistrationIdFormat
    ):
        self.car_registry = car_registry
        self.registration_id_format = registration_id_format
        self.failure_scores: dict[str, int] = {}
        self.car_passed = True
        self.car_stream: Subject[CarSnapshot] = Subject()
        (license_plate_monitor.get_registration_id_stream()
         .subscribe(lambda car_snapshot: self.on_next(car_snapshot)))

    def on_next(self, car_snapshot: CarSnapshot):
        registration_id = self.registration_id_format.preformat(car_snapshot.registration_id)
        print(registration_id)  # TODO: Comment this out
        if not self.registration_id_format.valid(registration_id):
            return

        try:
            if self.car_passed:
                car = self.car_registry.get_car(registration_id)
                car_snapshot = replace(car_snapshot, car=car)
                self.car_stream.on_next(car_snapshot)
                self.car_passed = False

        except CarNotFoundError:
            new_score = self.failure_scores.get(registration_id, 0) + 1
            self.failure_scores[registration_id] = new_score

            if self.failure_scores[registration_id] >= self.failing_score:
                self.failure_scores = {}
                self.car_stream.on_next(car_snapshot)

    def get_car_stream(self) -> Observable[CarSnapshot]:
        return self.car_stream

    def mark_car_as_passed(self):
        self.car_passed = True

