from abc import ABC, abstractmethod


class TextCorrector(ABC):
    @abstractmethod
    def get_possible_texts(self, original: str) -> list[str]:
        pass
