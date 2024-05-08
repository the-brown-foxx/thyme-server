from abc import ABC, abstractmethod
from service.registry.model.car import Car


class CarAuthenticator(ABC):
    @abstractmethod
    def authenticate_car(self, registration_id: Car):
        pass
