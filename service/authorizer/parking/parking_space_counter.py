from abc import ABC, abstractmethod
from service.authorizer.parking.model.parking_space_count import ParkingSpaceCount


class ParkingSpaceCounter(ABC):

    @abstractmethod
    def get_parking_space_count(self) -> ParkingSpaceCount:
        pass

    @abstractmethod
    def set_parking_space_count(self, parking_space_count: ParkingSpaceCount):
        pass

    @abstractmethod
    def increment_available_space(self):
        pass

    @abstractmethod
    def decrement_available_space(self):
        pass
