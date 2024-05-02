from typing import Optional

from service.registry.model.car import Car
from service.registry.repository.car_repository import CarRepository


class DummyCarRepository(CarRepository):

    cars: list[Car] = []

    def get_cars(self) -> list[Car]:
        return self.cars

    def get_car(self, registration_id: str) -> Optional[Car]:
        try:
            return list(filter(lambda car: car.registration_id == registration_id, self.cars))[0]
        except IndexError:
            return None

    def upsert_car(self, car: Car):
        self.delete_car(car.registration_id)
        self.cars.append(car)

    def delete_car(self, registration_id: str):
        self.cars = list(filter(lambda car: car.registration_id != registration_id, self.cars))
