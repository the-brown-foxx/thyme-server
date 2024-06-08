from dataclasses import dataclass
from abc import ABC

from hash.hashed_str import HashedStr


class Car(ABC):
    registration_id: str
    make: str
    model: str
    year: int
    color: str
    owner: str

    def to_dict(self) -> dict:
        dictionary = {
            'registration_id': self.registration_id,
            'make': self.make,
            'model': self.model,
            'year': self.year,
            'color': self.color,
            'owner': self.owner,
        }

        if isinstance(self, SetPasswordCar):
            dictionary['password'] = {
                'value': self.password.value,
                'salt': self.password.salt,
            }

        if isinstance(self, UnsetPasswordCar):
            dictionary['temporary_password'] = self.temporary_password

        return dictionary


@dataclass
class SetPasswordCar(Car):
    registration_id: str
    make: str
    model: str
    year: int
    color: str
    owner: str
    password: HashedStr


@dataclass
class UnsetPasswordCar(Car):
    registration_id: str
    make: str
    model: str
    year: int
    color: str
    owner: str
    temporary_password: str
