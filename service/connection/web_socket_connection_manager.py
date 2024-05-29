from typing import Optional

from fastapi import WebSocket

from service.connection.connection_manager import ConnectionManager


class WebSocketConnectionManager(ConnectionManager):
    web_socket: Optional[WebSocket]

    def __init__(self, web_socket: Optional[WebSocket] = None):
        self.web_socket = web_socket

    async def connect(self):
        if self.web_socket is not None:
            await self.web_socket.accept()

    async def disconnect(self):
        pass

    async def send_message(self, message):
        if self.web_socket is not None:
            await self.web_socket.send_json(message)
