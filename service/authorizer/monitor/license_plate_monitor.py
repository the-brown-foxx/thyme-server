from abc import ABC, abstractmethod


class LicensePlateMonitor(ABC):
    @abstractmethod
    def run(self):
        pass
