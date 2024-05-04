from abc import ABC, abstractmethod
from typing import Optional

from service.registry.model.car import Car
from service.registry.model.new_car import NewCar
from service.registry.model.car_update import CarUpdate


class CarRegistry(ABC):

    @abstractmethod
    def get_cars(self) -> list[Car]:
        pass

    @abstractmethod
    def get_car(self, registration_id: str) -> Optional[Car]:
        pass

    @abstractmethod
    def register_car(self, car: NewCar):
        pass

    @abstractmethod
    def update_car(self, car: CarUpdate):
        pass

    @abstractmethod
    def unregister_car(self, registration_id: str):
        pass
