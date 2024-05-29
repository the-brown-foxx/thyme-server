from abc import ABC, abstractmethod


class ConnectionManager(ABC):
    @abstractmethod
    async def connect(self):
        pass

    @abstractmethod
    async def disconnect(self):
        pass

    @abstractmethod
    async def send_message(self, message):
        pass
