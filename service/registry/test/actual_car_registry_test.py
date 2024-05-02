import unittest
from dataclasses import replace

from service.registry.actual_car_registry import ActualCarRegistry
from service.registry.model.car import Car
from service.registry.repository.dummy_car_repository import DummyCarRepository


# TODO: (Note to self by Jack Norris) Incorporate Blythe's error validation
class MyTestCase(unittest.TestCase):
    car_registry = ActualCarRegistry(DummyCarRepository())
    preregistered_cars = [
        Car(
            registration_id="4",
            make="McLaren",
            model="MCL38",
            year=2024,
            owner="Lando Norris",
            password="I love Carlos",
            password_temporary=False,
        ),
        Car(
            registration_id="55",
            make="Ferrari",
            model="SF-24",
            year=2024,
            owner="Carlos Sainz",
            password="I love Lando",
            password_temporary=False,
        ),
    ]

    def setUp(self):
        for preregistered_car in self.preregistered_cars:
            self.car_registry.upsert_car(preregistered_car)

    def test_get_cars(self):
        self.assertListEqual(self.preregistered_cars, self.car_registry.get_cars())

    def test_get_car(self):
        self.assertEqual(
            self.preregistered_cars[0],
            self.car_registry.get_car(self.preregistered_cars[0].registration_id),
        )
        self.assertEqual(
            self.preregistered_cars[1],
            self.car_registry.get_car(self.preregistered_cars[1].registration_id),
        )

    def test_insert_car(self):
        new_car = Car(
            registration_id="16",
            make="Ferrari",
            model="SF-24",
            year=2024,
            owner="Charles Leclerc",
            password="I love Carlos",
            password_temporary=False,
        )

        self.car_registry.upsert_car(new_car)
        self.assertEqual(new_car, self.car_registry.get_car(new_car.registration_id))

    def test_update_car(self):
        updated_car = replace(self.preregistered_cars[0], password="I miss you, Carlos")

        self.car_registry.upsert_car(updated_car)
        self.assertEqual(updated_car, self.car_registry.get_car(self.preregistered_cars[0].registration_id))

    def test_delete_car(self):
        self.car_registry.delete_car(self.preregistered_cars[0].registration_id)
        self.assertListEqual(self.preregistered_cars[1:], self.car_registry.get_cars())


if __name__ == '__main__':
    unittest.main()
