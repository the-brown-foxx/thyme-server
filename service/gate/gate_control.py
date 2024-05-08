from abc import ABC, abstractmethod


class GateControl(ABC):
    @abstractmethod
    def open_gate(self):
        pass

    @abstractmethod
    def close_gate(self):
        pass
