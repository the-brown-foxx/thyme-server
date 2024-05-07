from abc import ABC, abstractmethod

from service.authenticator.token.model.token import Token


class TokenProcessor(ABC):
    @abstractmethod
    def encode_token(self, payload: dict) -> Token:
        pass

    @abstractmethod
    def decode_token(self, token: Token) -> dict:
        pass
