from abc import ABC, abstractmethod


class DisplayController(ABC):
    @abstractmethod
    def show_instructions(self):
        pass

    @abstractmethod
    def show_car_info(self):
        pass

    @abstractmethod
    def show_unauthorized_message(self):
        pass
