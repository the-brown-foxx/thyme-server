from abc import ABC, abstractmethod

from reactivex import Observable

from service.authorizer.monitor.model.car_snapshot import CarSnapshot


class CarMonitor(ABC):
    @abstractmethod
    def get_car_stream(self) -> Observable[CarSnapshot]:
        pass

    @abstractmethod
    def mark_car_as_passed(self):
        pass
