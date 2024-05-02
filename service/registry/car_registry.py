from abc import ABC, abstractmethod
from typing import Optional

from service.registry.model.car import Car


class CarRegistry(ABC):

    @abstractmethod
    def get_cars(self) -> list[Car]:
        pass

    @abstractmethod
    def get_car(self, registration_id: str) -> Optional[Car]:
        pass

    @abstractmethod
    def upsert_car(self, car: Car):
        pass

    @abstractmethod
    def delete_car(self, registration_id: str):
        pass
