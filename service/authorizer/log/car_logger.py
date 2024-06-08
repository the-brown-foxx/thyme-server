from abc import ABC, abstractmethod

from reactivex import Observable

from service.authorizer.log.model.car_log import CarLog


class CarLogger(ABC):
    @abstractmethod
    def get_live_logs(self) -> Observable[list[CarLog]]:
        pass

    @abstractmethod
    def get_logs(self) -> list[CarLog]:
        pass

    @abstractmethod
    def get_logs_by_car_registration_id(self, car_registration_id: str) -> list[CarLog]:
        pass

    @abstractmethod
    def log(self, car_registration_id: str, entering: bool):
        pass
