from reactivex import Observable, Subject
from reactivex.subject import BehaviorSubject

from generator.generate_password import generate_password
from hash.hashed_str import hash_str
from service.exception import CarNotFoundError, FieldCannotBeBlankError, PasswordTooShortError, \
    RegistrationIdTakenError
from service.registry.car_registry import CarRegistry
from service.registry.model.car import Car, UnsetPasswordCar, SetPasswordCar
from service.registry.model.car_update import CarUpdate
from service.registry.model.new_car import NewCar
from service.registry.repository.car_repository import CarRepository


class ActualCarRegistry(CarRegistry):
    car_repository: CarRepository

    cars: Subject[list[Car]]

    def __init__(self, car_repository: CarRepository):
        self.car_repository = car_repository
        self.cars = BehaviorSubject(self.get_cars())

    def update_live_cars(self):
        self.cars.on_next(self.get_cars())

    def get_live_cars(self) -> Observable[list[Car]]:
        return self.cars

    def get_cars(self) -> list[Car]:
        return self.car_repository.get_cars()

    def get_car(self, registration_id: str) -> Car:
        car = self.car_repository.get_car(registration_id)
        if car is None:
            raise CarNotFoundError(registration_id)

        return car

    def register_car(self, new_car: NewCar):
        if self.car_repository.get_car(new_car.registration_id) is not None:
            raise RegistrationIdTakenError(new_car.registration_id)

        if new_car.registration_id == "":
            raise FieldCannotBeBlankError("registration_id")
        if new_car.make == "":
            raise FieldCannotBeBlankError("make")
        if new_car.model == "":
            raise FieldCannotBeBlankError("model")
        if new_car.year < 0:  # year is set by the UI to -1 when it's empty
            raise FieldCannotBeBlankError("year")
        if new_car.color == "":
            raise FieldCannotBeBlankError("color")
        if new_car.owner == "":
            raise FieldCannotBeBlankError("owner")

        unset_password_car = UnsetPasswordCar(
            registration_id=new_car.registration_id,
            make=new_car.make,
            model=new_car.model,
            year=new_car.year,
            color=new_car.color,
            owner=new_car.owner,
            temporary_password=generate_password(),
        )
        self.car_repository.upsert_car(unset_password_car)
        self.update_live_cars()

    def update_car(self, car_update: CarUpdate):
        if car_update.registration_id == "":
            raise FieldCannotBeBlankError("registration_id")
        if car_update.make == "":
            raise FieldCannotBeBlankError("make")
        if car_update.model == "":
            raise FieldCannotBeBlankError("model")
        if car_update.year < 0:  # year is set by the UI to -1 when it's empty
            raise FieldCannotBeBlankError("year")
        if car_update.color == "":
            raise FieldCannotBeBlankError("color")
        if car_update.owner == "":
            raise FieldCannotBeBlankError("owner")
        if car_update.password is not None and len(car_update.password) < 8:
            raise PasswordTooShortError()

        old_car = self.car_repository.get_car(car_update.registration_id)

        if old_car is None:
            raise CarNotFoundError(car_update.registration_id)

        registration_id = car_update.registration_id if car_update.registration_id is not None \
            else old_car.registration_id
        make = car_update.make if car_update.make is not None else old_car.make
        model = car_update.model if car_update.model is not None else old_car.model
        year = car_update.year if car_update.year is not None else old_car.year
        color = car_update.color if car_update.color is not None else old_car.color
        owner = car_update.owner if car_update.owner is not None else old_car.owner

        if isinstance(old_car, UnsetPasswordCar) and car_update.password is None:
            new_car = UnsetPasswordCar(
                registration_id=registration_id,
                make=make,
                model=model,
                year=year,
                color=color,
                owner=owner,
                temporary_password=old_car.temporary_password,
            )
            self.car_repository.upsert_car(new_car)
        else:
            new_car = SetPasswordCar(
                registration_id=registration_id,
                make=make,
                model=model,
                year=year,
                color=color,
                owner=owner,
                password=old_car.password if isinstance(old_car, SetPasswordCar) else hash_str(car_update.password),
            )
            self.car_repository.upsert_car(new_car)

        self.update_live_cars()

    def unregister_car(self, registration_id: str):
        if self.car_repository.get_car(registration_id) is None:
            raise CarNotFoundError(registration_id)
        else:
            self.car_repository.delete_car(registration_id)

        self.update_live_cars()
