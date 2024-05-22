from abc import ABC, abstractmethod
from threading import Thread

from reactivex import Observable


class LicensePlateMonitor(ABC):
    @abstractmethod
    def get_registration_id_stream(self) -> Observable[str]:
        pass

    @abstractmethod
    def get_thread(self) -> Thread:
        pass
