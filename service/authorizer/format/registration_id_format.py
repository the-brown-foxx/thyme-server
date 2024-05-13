from abc import ABC, abstractmethod


class RegistrationIdFormat(ABC):
    @abstractmethod
    def valid(self, registration_id: str):
        pass
