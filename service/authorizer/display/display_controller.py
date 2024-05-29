from abc import ABC, abstractmethod

from service.registry.model.car import Car


class DisplayController(ABC):
    @abstractmethod
    def update_vacant_space(self, vacant_space: int):
        pass

    @abstractmethod
    def show_instructions(self):
        pass

    @abstractmethod
    def show_car_info(self, car: Car):
        pass

    @abstractmethod
    def show_unauthorized_message(self, registration_id: str):
        pass
