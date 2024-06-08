from fastapi import WebSocket

from service.authenticator.admin.admin_authenticator import AdminAuthenticator
from sockets.exception_handler import handle_websocket_exception


class WebsocketManager:
    def __init__(self, admin_authenticator: AdminAuthenticator):
        self.active_connections: list[WebSocket] = []
        self.admin_authenticator = admin_authenticator

    async def connect(self, websocket: WebSocket) -> bool:
        await websocket.accept()

        token = None
        message = await websocket.receive_json()  # TODO: Add a timeout?

        if message['action'] == 'authenticate':
            token = message['token']

        error = await handle_websocket_exception(
            websocket,
            lambda: self.admin_authenticator.require_authentication(token),
        )

        if error is not None:
            await websocket.close()
            return False

        self.active_connections.append(websocket)
        await websocket.send_json({'status': 'CONNECTED'})
        return True

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, message: dict):
        for connection in self.active_connections:
            await connection.send_json(message)
