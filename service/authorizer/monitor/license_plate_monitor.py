from abc import ABC, abstractmethod

from reactivex import Observable


class LicensePlateMonitor(ABC):
    @abstractmethod
    def get_registration_id_stream(self) -> Observable[str]:
        pass
