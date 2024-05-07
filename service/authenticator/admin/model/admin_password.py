from dataclasses import dataclass

from hash.hashed_str import HashedStr


@dataclass
class AdminPassword:
    hash: HashedStr
    version: int
