from dataclasses import dataclass
from hashlib import sha512
from os import urandom


@dataclass
class HashedStr:
    value: str
    salt: str


def hash_str(plaintext: str, salt: str = urandom(16).hex()) -> HashedStr:
    return HashedStr(
        value=sha512(plaintext.encode() + salt.encode()).hexdigest(),
        salt=salt,
    )


def hash_matches(hashed_str: HashedStr, plaintext: str) -> bool:
    return hash_str(plaintext=plaintext, salt=hashed_str.salt).value == hashed_str.value
