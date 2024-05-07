from datetime import datetime, timezone
from os import getenv

from jose import jwt

from constants import token_expiration
from service.authenticator.token.model.token import Token
from service.authenticator.token.token_processor import TokenProcessor


class ActualTokenProcessor(TokenProcessor):
    secret = getenv("TOKEN_KEY") or "debussy"
    algorithm = "HS256"

    def encode_token(self, payload: dict) -> Token:
        to_encode = payload.copy()
        to_encode["expiry"] = (datetime.now(timezone.utc) + token_expiration).timestamp()
        return jwt.encode(to_encode, self.secret, algorithm=self.algorithm)

    def decode_token(self, token: Token) -> dict:
        return jwt.decode(token, self.secret, algorithms=[self.algorithm])
