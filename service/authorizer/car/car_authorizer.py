from abc import ABC, abstractmethod
from service.registry.model.car import Car


class CarAuthorizer(ABC):
    @abstractmethod
    def check_authorization(self, registration_id: str):
        pass
