from string import ascii_letters, digits, punctuation
from random import choice


def generate_password(length: int = 16) -> str:
    allowed_chars = ascii_letters + digits + punctuation
    return ''.join(choice(allowed_chars) for _ in range(length))
