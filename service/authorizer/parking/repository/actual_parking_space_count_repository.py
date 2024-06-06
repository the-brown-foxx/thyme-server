from typing import Optional

from peewee import DoesNotExist

from service.authorizer.parking.model.parking_space_count import ParkingSpaceCount
from service.authorizer.parking.repository.parking_space_count_entity import ParkingSpaceCountEntity
from service.authorizer.parking.repository.parking_space_count_repository import ParkingSpaceCountRepository


class ActualParkingSpaceCountRepository(ParkingSpaceCountRepository):
    ParkingSpaceCountEntity.create_table(safe=True)

    def get_parking_space_count(self) -> Optional[ParkingSpaceCount]:
        try:
            parking_space_count = ParkingSpaceCountEntity.get()
            return ParkingSpaceCount(
                total_space=parking_space_count.total_space,
                vacant_space=parking_space_count.vacant_space,
            )
        except DoesNotExist:
            return None

    def upsert(self, parking_space_count: ParkingSpaceCount):
        try:
            old_parking_space_count_entity: ParkingSpaceCountEntity = ParkingSpaceCountEntity.get()
            old_parking_space_count_entity.total_space = parking_space_count.total_space
            old_parking_space_count_entity.vacant_space = parking_space_count.vacant_space
            old_parking_space_count_entity.save()
        except DoesNotExist:
            ParkingSpaceCountEntity(
                total_space=parking_space_count.total_space,
                vacant_space=parking_space_count.vacant_space,
            ).save()
