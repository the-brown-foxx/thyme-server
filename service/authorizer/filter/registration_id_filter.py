from abc import ABC, abstractmethod

from reactivex import Observable


class RegistrationIdFilter(ABC):
    @abstractmethod
    def get_filtered_stream(self, stream: Observable[str]) -> Observable[str]:
        pass
