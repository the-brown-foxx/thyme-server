from abc import ABC, abstractmethod
from threading import Thread

from reactivex import Observable

from service.authorizer.monitor.model.car_snapshot import CarSnapshot


class LicensePlateMonitor(ABC):
    @abstractmethod
    def get_registration_id_stream(self) -> Observable[CarSnapshot]:
        pass

    @abstractmethod
    def get_thread(self) -> Thread:
        pass
