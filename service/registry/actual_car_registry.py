from service.registry.car_registry import CarRegistry
from service.registry.model.car import Car
from service.registry.repository.car_repository import CarRepository
from service.registry.exception.get_car_exception import CarNotFound


# TODO: implement these please uwu
class ActualCarRegistry(CarRegistry):
    car_repository: CarRepository

    def __init__(self, car_repository: CarRepository):
        self.car_repository = car_repository

    def get_cars(self) -> list[Car]:
        return self.car_repository.get_cars()

    def get_car(self, registration_id: str) -> Car:
        car = self.car_repository.get_car(registration_id)
        if car is None:
            raise CarNotFound(registration_id)
        else:
            return car

    def upsert_car(self, car: Car):
        # TODO: Add proper validation here like checking if the password is too short etc.
        # TODO: Write individual exception for each validation error
        self.car_repository.upsert_car(car)

    def delete_car(self, registration_id: str):
        # TODO: Add proper validation here
        self.car_repository.delete_car(registration_id)
