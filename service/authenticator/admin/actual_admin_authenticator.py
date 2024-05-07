from datetime import datetime, timezone
from random import randint
from typing import Optional

from jose import JWTError

from constants import min_password_length
from hash.hashed_str import hash_matches, hash_str
from service.authenticator.admin.admin_authenticator import AdminAuthenticator
from service.authenticator.admin.model.admin_password import AdminPassword
from service.authenticator.admin.repository.admin_password_repository import AdminPasswordRepository
from service.authenticator.token.model.token import Token
from service.authenticator.token.token_processor import TokenProcessor
from service.exception import IncorrectPasswordError, PasswordTooShortError, InvalidTokenError


class ActualAdminAuthenticator(AdminAuthenticator):
    admin_password_repository: AdminPasswordRepository
    token_processor: TokenProcessor

    def __init__(self, admin_password_repository: AdminPasswordRepository, token_processor: TokenProcessor):
        self.admin_password_repository = admin_password_repository
        self.token_processor = token_processor

    def password_set(self) -> bool:
        return self.admin_password_repository.get_password() is not None

    def login(self, password: str) -> Token:
        saved_password = self.admin_password_repository.get_password()
        if saved_password is None or not hash_matches(saved_password.hash, password):
            raise IncorrectPasswordError()

        claim = {
            'username': 'admin',
            'password_version': saved_password.version,
        }

        return self.token_processor.encode_token(claim)

    def change_password(self, old_password: Optional[str], new_password: str):
        saved_password = self.admin_password_repository.get_password()

        if saved_password is not None and (old_password is None or not hash_matches(saved_password.hash, old_password)):
            raise IncorrectPasswordError()

        if len(new_password) < min_password_length:
            raise PasswordTooShortError()

        new_password = AdminPassword(
            hash=hash_str(new_password),
            version=randint(-2147483648, 2147483647),
        )

        self.admin_password_repository.update_password(new_password)

    def require_authentication(self, token: Token):
        try:
            claim = self.token_processor.decode_token(token)
            saved_password = self.admin_password_repository.get_password()

            if saved_password is None or claim['password_version'] != saved_password.version:
                raise IncorrectPasswordError()

            # TODO: Find a way to unit test this?
            if claim['expiry'] <= datetime.now(timezone.utc).timestamp():
                raise InvalidTokenError()

        except JWTError:
            raise InvalidTokenError()
