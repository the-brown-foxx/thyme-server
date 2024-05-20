from abc import ABC, abstractmethod
from typing import Optional

from service.authenticator.log.model.car_log import CarLog


class CarLogRepository(ABC):

    @abstractmethod
    def get_logs(self) -> list[CarLog]:
        pass

    @abstractmethod
    def get_logs_by_car_registration_id(self, registration_id: str) -> list[CarLog]:
        pass

    @abstractmethod
    def upsert_log(self, car_log: CarLog):
        pass
