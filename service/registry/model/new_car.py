from dataclasses import dataclass


@dataclass
class NewCar:
    registration_id: str
    make: str
    model: str
    year: int
    color: str
    owner: str
