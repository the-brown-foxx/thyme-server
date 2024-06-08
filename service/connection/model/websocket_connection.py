from typing import Optional

from fastapi import WebSocket

from service.authenticator.token.model.token import Token


class WebsocketConnection:
    def __init__(self, websocket: WebSocket, token: Optional[Token]):
        self.websocket = websocket
        self.token = token
