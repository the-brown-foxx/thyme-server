from abc import ABC, abstractmethod

from reactivex.subject import BehaviorSubject


class LicensePlateMonitor(ABC):
    @abstractmethod
    def get_license_plate_stream(self) -> BehaviorSubject[str]:
        pass
