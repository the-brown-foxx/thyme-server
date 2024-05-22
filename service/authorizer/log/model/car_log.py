from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional


@dataclass
class CarLog:
    date_time: datetime
    car_registration_id: str
    entering: bool
    image: str
    sus: bool
    log_id: Optional[int] = field(default=None)
