from fastapi import WebSocket, WebSocketDisconnect

from service.authorizer.log.car_logger import CarLogger
from service.authorizer.log.model.car_log import CarLog
from service.connection.websocket_manager import WebsocketManager
from sockets.run_async import run_async


async def handle_car_logger_websocket(
        websocket_manager: WebsocketManager,
        car_logger: CarLogger,
        websocket: WebSocket,
):
    connection_successful = await websocket_manager.connect(websocket)

    if not connection_successful:
        return

    async def async_on_next_logs(logs: list[CarLog]):
        await websocket_manager.broadcast({
            'action': 'show_logs',
            'logs': [log.to_dict() for log in logs],
        })

    def on_next_logs(logs: list[CarLog]):
        run_async(async_on_next_logs(logs))

    car_logger.get_live_logs().subscribe(on_next_logs)

    try:
        while True:
            await websocket.receive_text()

    except WebSocketDisconnect:
        await websocket_manager.disconnect(websocket)
