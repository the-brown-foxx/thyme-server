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

    def to_dict(self) -> dict:
        return {
            'log_id': self.log_id,
            'date_time': self.date_time.isoformat(),
            'car_registration_id': self.car_registration_id,
            'entering': self.entering,
            'image': self.image,
            'sus': self.sus,
        }
