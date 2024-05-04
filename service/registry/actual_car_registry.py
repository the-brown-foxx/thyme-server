from generator.generate_password import generate_password
from service.registry.car_registry import CarRegistry
from service.registry.model.car import Car, UnsetPasswordCar
from service.registry.model.car_update import CarUpdate
from service.registry.model.exception import CarNotFoundError
from service.registry.model.new_car import NewCar
from service.registry.repository.car_repository import CarRepository


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
            raise CarNotFoundError(registration_id)
        else:
            return car

    def register_car(self, new_car: NewCar):
        unset_password_car = UnsetPasswordCar(
            registration_id=new_car.registration_id,
            make=new_car.make,
            model=new_car.model,
            year=new_car.year,
            owner=new_car.owner,
            temporary_password=generate_password(),
        )
        self.car_repository.upsert_car(unset_password_car)

    def update_car(self, car_update: CarUpdate):
        old_car = self.car_repository.get_car(car_update.registration_id)
        if old_car is None:
            raise CarNotFoundError(car_update.registration_id)
        else:
            if isinstance(old_car, UnsetPasswordCar):
                if car_update.password is None:
                    new_car = UnsetPasswordCar(
                        registration_id=car_update.registration_id,
                        make=car_update.make,
                        model=car_update.model,
                        year=car_update.year,
                        owner=car_update.owner,
                        temporary_password=old_car.temporary_password,
                    )
        # TODO: Unfinished

    def unregister_car(self, registration_id: str):
        # TODO: Add proper validation here
        self.car_repository.delete_car(registration_id)
