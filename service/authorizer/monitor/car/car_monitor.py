from abc import ABC, abstractmethod
from typing import Union

from reactivex import Observable

from service.registry.model.car import Car


class CarMonitor(ABC):
    @abstractmethod
    def get_car_stream(self) -> Observable[Union[Car, str]]:
        pass

    @abstractmethod
    def mark_car_as_passed(self):
        pass
