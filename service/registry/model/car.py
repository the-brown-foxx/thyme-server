from dataclasses import dataclass


@dataclass
class Car:
    registration_id: str
    make: str
    model: str
    year: int
    owner: str
    password: str
    password_temporary: bool
