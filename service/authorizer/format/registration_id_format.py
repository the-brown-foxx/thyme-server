from abc import ABC, abstractmethod


class RegistrationIdFormat(ABC):
    @abstractmethod
    def preformat(self, registration_id: str):
        pass

    @abstractmethod
    def valid(self, registration_id: str):
        pass
