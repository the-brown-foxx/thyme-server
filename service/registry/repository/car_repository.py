from abc import ABC, abstractmethod

from service.registry.model.car import Car


class CarRepository(ABC):

    @abstractmethod
    def get_cars(self) -> list[Car]:
        pass

    @abstractmethod
    def get_car(self, registration_id: str) -> Car:
        pass

    @abstractmethod
    def upsert_car(self, car: Car):
        pass

    @abstractmethod
    def delete_car(self, registration_id: str):
        pass
