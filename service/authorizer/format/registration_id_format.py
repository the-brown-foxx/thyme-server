from abc import ABC, abstractmethod


class RegistrationIdFormat(ABC):
    @abstractmethod
    def preformat(self, registration_id: str) -> str:
        pass

    @abstractmethod
    def valid(self, registration_id: str) -> bool:
        pass
