from dataclasses import dataclass


@dataclass
class ParkingSpaceCount:
    total_space: int
    vacant_space: int

    def to_dict(self):
        return {
            'total_space': self.total_space,
            'vacant_space': self.vacant_space,
        }
