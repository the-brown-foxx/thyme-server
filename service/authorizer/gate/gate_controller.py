from abc import ABC, abstractmethod


class GateController(ABC):
    @abstractmethod
    def open_gate(self):
        pass
