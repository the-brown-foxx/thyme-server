from abc import ABC, abstractmethod
from typing import Optional

from service.authenticator.token.model.token import Token


class AdminAuthenticator(ABC):
    @abstractmethod
    def password_set(self) -> bool:
        pass

    @abstractmethod
    def login(self, password: str) -> Token:
        pass

    @abstractmethod
    def change_password(self, old_password: Optional[str], new_password: str):
        pass

    @abstractmethod
    def require_authentication(self, token: Token):
        pass
