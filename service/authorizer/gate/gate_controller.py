from abc import ABC, abstractmethod

from reactivex import Observable


class GateController(ABC):
    @abstractmethod
    def open_gate(self) -> Observable[bool]:
        pass
