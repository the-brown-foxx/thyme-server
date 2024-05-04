import unittest

from hash.hashed_str import hash_matches
from service.registry.actual_car_registry import ActualCarRegistry
from service.registry.model.car import SetPasswordCar
from service.registry.model.car_update import CarUpdate
from service.registry.model.exception import CarNotFoundError, FieldCannotBeBlankError
from service.registry.model.new_car import NewCar
from service.registry.repository.dummy_car_repository import DummyCarRepository


class ActualCarRegistryTest(unittest.TestCase):
    car_registry = ActualCarRegistry(DummyCarRepository())
    preregistered_cars = [
        NewCar(
            registration_id="4",
            make="McLaren",
            model="MCL38",
            year=2024,
            owner="Lando Norris",
        ),
        NewCar(
            registration_id="55",
            make="Ferrari",
            model="SF-24",
            year=2024,
            owner="Carlos Sainz",
        ),
    ]

    def setUp(self):
        for preregistered_car in self.preregistered_cars:
            self.car_registry.register_car(preregistered_car)

    def test_get_cars(self):
        registered_cars = self.car_registry.get_cars()
        self.assertEqual(len(self.preregistered_cars), len(registered_cars))
        for index in range(len(self.preregistered_cars)):
            registered_car = registered_cars[index]
            self.assertEqual(
                self.preregistered_cars[index],
                NewCar(
                    registration_id=registered_car.registration_id,
                    make=registered_car.make,
                    model=registered_car.model,
                    year=registered_car.year,
                    owner=registered_car.owner,
                ),
            )

    def test_get_car(self):
        for index in range(len(self.preregistered_cars)):
            registered_car = self.car_registry.get_car(self.preregistered_cars[index].registration_id)
            self.assertEqual(
                self.preregistered_cars[index],
                NewCar(
                    registration_id=registered_car.registration_id,
                    make=registered_car.make,
                    model=registered_car.model,
                    year=registered_car.year,
                    owner=registered_car.owner,
                ),
            )

    def test_get_car_car_not_found(self):
        with self.assertRaises(CarNotFoundError):
            self.car_registry.get_car("99")

    def test_register_car(self):
        new_car = NewCar(
            registration_id="16",
            make="Ferrari",
            model="SF-24",
            year=2024,
            owner="Charles Leclerc",
        )

        self.car_registry.register_car(new_car)
        newly_registered_car = self.car_registry.get_car(new_car.registration_id)
        self.assertEqual(
            new_car,
            NewCar(
                registration_id=newly_registered_car.registration_id,
                make=newly_registered_car.make,
                model=newly_registered_car.model,
                year=newly_registered_car.year,
                owner=newly_registered_car.owner,
            ),
        )

    def test_register_car_field_cannot_be_blank(self):
        with self.assertRaises(FieldCannotBeBlankError) as error_context:
            self.car_registry.register_car(
                NewCar(
                    registration_id="",
                    make="Ferrari",
                    model="SF-24",
                    year=2024,
                    owner="Charles Leclerc",
                )
            )

            error_context.exception.field_name = "registration_id"

        with self.assertRaises(FieldCannotBeBlankError) as error_context:
            self.car_registry.register_car(
                NewCar(
                    registration_id="16",
                    make="",
                    model="SF-24",
                    year=2024,
                    owner="Charles Leclerc",
                )
            )

            error_context.exception.field_name = "make"

        with self.assertRaises(FieldCannotBeBlankError) as error_context:
            self.car_registry.register_car(
                NewCar(
                    registration_id="16",
                    make="Ferrari",
                    model="",
                    year=2024,
                    owner="Charles Leclerc",
                )
            )

            error_context.exception.field_name = "model"

        with self.assertRaises(FieldCannotBeBlankError) as error_context:
            self.car_registry.register_car(
                NewCar(
                    registration_id="16",
                    make="Ferrari",
                    model="SF-24",
                    year=2024,
                    owner="",
                )
            )

            error_context.exception.field_name = "owner"

    def test_update_car(self):
        registration_id = self.preregistered_cars[0].registration_id

        new_make = "Red Bull"
        car_update = CarUpdate(
            registration_id=registration_id,
            make=new_make,
        )
        self.car_registry.update_car(car_update)
        updated_car = self.car_registry.get_car(registration_id)
        self.assertEqual(updated_car.make, new_make)

    def test_update_car_field_should_not_affect_other_fields(self):
        registration_id = self.preregistered_cars[1].registration_id
        new_owner = "Lewis Hamilton"
        new_year = 2025
        car_update = CarUpdate(
            registration_id=registration_id,
            owner=new_owner,
            year=new_year,
        )
        self.car_registry.update_car(car_update)
        updated_car = self.car_registry.get_car(registration_id)
        self.assertEqual(updated_car.owner, new_owner)
        self.assertEqual(updated_car.year, new_year)
        self.assertEqual(updated_car.make, self.preregistered_cars[1].make)
        self.assertEqual(updated_car.model, self.preregistered_cars[1].model)

    def test_update_car_should_update_password(self):
        registration_id = self.preregistered_cars[0].registration_id
        new_password = "new_password"
        car_update = CarUpdate(
            registration_id=registration_id,
            password=new_password,
        )
        self.car_registry.update_car(car_update)
        updated_car = self.car_registry.get_car(registration_id)
        self.assertIs(type(updated_car), SetPasswordCar)
        assert isinstance(updated_car, SetPasswordCar)
        self.assertTrue(hash_matches(updated_car.password, new_password))

    def test_update_car_field_cannot_be_blank(self):
        with self.assertRaises(FieldCannotBeBlankError) as error_context:
            self.car_registry.update_car(
                CarUpdate(
                    registration_id="",
                    make="Ferrari",
                )
            )

            error_context.exception.field_name = "registration_id"

        with self.assertRaises(FieldCannotBeBlankError) as error_context:
            self.car_registry.update_car(
                CarUpdate(
                    registration_id="16",
                    make="",
                )
            )

            error_context.exception.field_name = "make"

        with self.assertRaises(FieldCannotBeBlankError) as error_context:
            self.car_registry.update_car(
                CarUpdate(
                    registration_id="16",
                    model="",
                )
            )

            error_context.exception.field_name = "model"

        with self.assertRaises(FieldCannotBeBlankError) as error_context:
            self.car_registry.update_car(
                CarUpdate(
                    registration_id="16",
                    owner="",
                )
            )

            error_context.exception.field_name = "owner"

        with self.assertRaises(FieldCannotBeBlankError) as error_context:
            self.car_registry.update_car(
                CarUpdate(
                    registration_id="16",
                    password="",
                )
            )

            error_context.exception.field_name = "password"

    def test_unregister_car(self):
        self.car_registry.unregister_car(self.preregistered_cars[0].registration_id)
        self.assertListEqual(self.preregistered_cars[1:], self.car_registry.get_cars())

    def test_unregister_car_car_not_found(self):
        with self.assertRaises(CarNotFoundError):
            self.car_registry.unregister_car("99")


if __name__ == '__main__':
    unittest.main()
