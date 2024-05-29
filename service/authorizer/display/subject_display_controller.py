from reactivex import Subject

from service.authorizer.display.display_controller import DisplayController
from service.authorizer.parking.parking_space_counter import ParkingSpaceCounter
from service.registry.model.car import Car

DisplayControllerEvent = None | Car | str | int


class SubjectDisplayController(DisplayController):
    subject: Subject[DisplayControllerEvent]

    def __init__(
            self,
            subject: Subject[DisplayControllerEvent],
            parking_space_counter: ParkingSpaceCounter,
    ):
        self.subject = subject
        vacant_space = parking_space_counter.get_parking_space_count().vacant_space
        self.update_vacant_space(vacant_space)

    def update_vacant_space(self, vacant_space: int):
        self.subject.on_next(vacant_space)

    def show_instructions(self):
        self.subject.on_next(None)

    def show_car_info(self, car: Car):
        self.subject.on_next(car)

    def show_unauthorized_message(self, registration_id: str):
        self.subject.on_next(registration_id)
