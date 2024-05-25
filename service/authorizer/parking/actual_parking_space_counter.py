from dataclasses import replace

from service.authorizer.parking.model.parking_space_count import ParkingSpaceCount
from service.authorizer.parking.parking_space_counter import ParkingSpaceCounter
from service.authorizer.parking.repository.parking_space_count_entity import ParkingSpaceCountEntity
from service.authorizer.parking.repository.parking_space_count_repository import ParkingSpaceCountRepository
from service.exception import UnsetParkingSpaceError, TotalSpaceIsLessThanVacantSpaceError, FieldCannotBeBlankError


class ActualParkingSpaceCounter(ParkingSpaceCounter):
    parking_space_repository: ParkingSpaceCountRepository

    def __init__(self, parking_space_repository: ParkingSpaceCountRepository):
        self.parking_space_repository = parking_space_repository

    def get_parking_space_count(self) -> ParkingSpaceCount:
        count = self.parking_space_repository.get_parking_space_count()
        if count is None:
            raise UnsetParkingSpaceError()
        return count

    def set_parking_space_count(self, parking_space_count: ParkingSpaceCount):
        if parking_space_count.total_space < 0:
            raise FieldCannotBeBlankError("total_space")
        if parking_space_count.vacant_space < 0:
            raise FieldCannotBeBlankError("vacant_space")
        if parking_space_count.total_space < parking_space_count.vacant_space:
            raise TotalSpaceIsLessThanVacantSpaceError()
        parking_counter = ParkingSpaceCount(
            total_space=parking_space_count.total_space,
            vacant_space=parking_space_count.vacant_space,
        )
        self.parking_space_repository.upsert(parking_counter)

    def parking_space_set(self) -> bool:
        return self.parking_space_repository.get_parking_space_count() is not None

    def increment_available_space(self):
        old_parking_space_count = self.get_parking_space_count()
        new_parking_space_count = replace(
            old_parking_space_count,
            vacant_space=old_parking_space_count.vacant_space + 1,
        )
        self.parking_space_repository.upsert(new_parking_space_count)

    def decrement_available_space(self):
        old_parking_space_count = self.get_parking_space_count()
        new_parking_space_count = replace(
            old_parking_space_count,
            vacant_space=old_parking_space_count.vacant_space - 1,
        )
        self.parking_space_repository.upsert(new_parking_space_count)
