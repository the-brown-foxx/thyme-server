from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class CarLog:
    log_id: Optional[int]
    date_time: datetime
    car_registration_id: str
    entering: bool
    image: str
    sus: bool
