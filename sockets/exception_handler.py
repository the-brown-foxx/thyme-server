from typing import Callable, Optional

from fastapi import WebSocket

from service.exception_handler import handle_exception


async def handle_websocket_exception(websocket: WebSocket, task: Callable) -> Optional[dict]:
    error = handle_exception(task)

    if error is not None:
        await websocket.send_json(error)

    return error
