from dataclasses import dataclass, field
from typing import Optional

from service.authorizer.recognition.detector.model.image import Image
from service.registry.model.car import Car


@dataclass
class CarSnapshot:
    registration_id: str
    snapshot: Image
    car: Optional[Car] = field(default=None)
