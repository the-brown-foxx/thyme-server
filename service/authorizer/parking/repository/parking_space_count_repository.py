from abc import ABC, abstractmethod
from typing import Optional

from service.authorizer.parking.model.parking_space_count import ParkingSpaceCount


class ParkingSpaceCountRepository(ABC):

    @abstractmethod
    def get_parking_space_count(self) -> Optional[ParkingSpaceCount]:
        pass

    @abstractmethod
    def upsert(self, parking_space_count: ParkingSpaceCount):
        pass
