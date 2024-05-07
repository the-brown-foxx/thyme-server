from typing import Optional

from service.registry.repository.car_entity import CarEntity
from service.registry.model.car import Car, SetPasswordCar, UnsetPasswordCar
from service.registry.repository.car_repository import CarRepository
from hash.hashed_str import HashedStr
from peewee import *


def car_entity_to_car(car_entity: CarEntity):
    return UnsetPasswordCar(
        registration_id=car_entity.registration_id,
        make=car_entity.make,
        model=car_entity.model,
        year=car_entity.year,
        owner=car_entity.owner,
        temporary_password=car_entity.temporary_password,
    ) if car_entity.temporary_password is not None else SetPasswordCar(
        registration_id=car_entity.registration_id,
        make=car_entity.make,
        model=car_entity.model,
        year=car_entity.year,
        owner=car_entity.owner,
        password=HashedStr(
            value=car_entity.password_hash,
            salt=car_entity.password_salt,
        ),
    )


def car_to_car_entity(car: Car):
    return CarEntity(
        registration_id=car.registration_id,
        make=car.make,
        model=car.model,
        year=car.year,
        owner=car.owner,
        temporary_password=car.temporary_password if isinstance(car, UnsetPasswordCar) else None,
        password_hash=car.password.value if isinstance(car, SetPasswordCar) else None,
        password_salt=car.password.salt if isinstance(car, SetPasswordCar) else None,
    )


class ActualCarRepository(CarRepository):
    CarEntity.create_table(safe=True)

    def get_cars(self) -> list[Car]:
        cars: list[Car] = []
        car_entities = CarEntity.select()

        for car_entity in car_entities:
            cars.append(car_entity_to_car(car_entity))

        return cars

    def get_car(self, registration_id: str) -> Optional[Car]:
        try:
            car_entity = CarEntity.get(CarEntity.registration_id == registration_id)
            return car_entity_to_car(car_entity)
        except DoesNotExist:
            return None

    def upsert_car(self, car: Car):
        new_car_entity = car_to_car_entity(car)

        try:
            old_car_entity = CarEntity.get(CarEntity.registration_id == car.registration_id)
            old_car_entity.make = new_car_entity.make
            old_car_entity.model = new_car_entity.model
            old_car_entity.year = new_car_entity.year
            old_car_entity.owner = new_car_entity.owner
            old_car_entity.temporary_password = new_car_entity.temporary_password
            old_car_entity.hash = new_car_entity.password_hash
            old_car_entity.salt = new_car_entity.password_salt
            old_car_entity.save()
        except DoesNotExist:
            new_car_entity.save()

    def delete_car(self, registration_id: str) -> Optional[int]:
        query = CarEntity.delete().where(CarEntity.registration_id == registration_id)
        return query.execute()
