from dataclasses import dataclass, field
from typing import Optional


@dataclass
class CarUpdate:
    registration_id: str
    make: Optional[str] = field(default=None)
    model: Optional[str] = field(default=None)
    year: Optional[int] = field(default=None)
    color: Optional[int] = field(default=None)
    owner: Optional[str] = field(default=None)
    password: Optional[str] = field(default=None)
