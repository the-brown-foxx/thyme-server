from dataclasses import dataclass
from abc import ABC

from hash.hashed_str import HashedStr


class Car(ABC):
    registration_id: str
    make: str
    model: str
    year: int
    owner: str


@dataclass
class SetPasswordCar(Car):
    registration_id: str
    make: str
    model: str
    year: int
    owner: str
    password: HashedStr


@dataclass
class UnsetPasswordCar(Car):
    registration_id: str
    make: str
    model: str
    year: int
    owner: str
    temporary_password: str
