from fastapi import WebSocket, WebSocketDisconnect

from service.authorizer.parking.model.parking_space_count import ParkingSpaceCount
from service.authorizer.parking.parking_space_counter import ParkingSpaceCounter
from service.connection.websocket_manager import WebsocketManager
from sockets.exception_handler import handle_websocket_exception
from service.run_async import run_async


async def handle_parking_space_counter_websocket(
        websocket_manager: WebsocketManager,
        parking_space_counter: ParkingSpaceCounter,
        websocket: WebSocket,
):
    connection_successful = await websocket_manager.connect(websocket)

    if not connection_successful:
        return

    async def async_on_next_parking_space_count(parking_space_count: ParkingSpaceCount):
        await websocket_manager.broadcast({
            'action': 'show_parking_space_count',
            'parking_space_count': parking_space_count.to_dict() if parking_space_count else None,
        })

    def on_next_parking_space_count(parking_space_count: ParkingSpaceCount):
        run_async(async_on_next_parking_space_count(parking_space_count))

    parking_space_counter.get_live_parking_space_count().subscribe(on_next_parking_space_count)

    def handle_action(_message: dict):
        match _message['action']:
            case 'update':
                parking_space_update = _message['parking_space_count']
                parking_space_count = ParkingSpaceCount(
                    total_space=parking_space_update['total_space'],
                    vacant_space=parking_space_update['vacant_space'],
                )
                parking_space_counter.set_parking_space_count(parking_space_count)
                run_async(websocket.send_json({"status": "SUCCESSFUL"}))

    try:
        while True:
            message = await websocket.receive_json()
            print(message)
            await handle_websocket_exception(websocket, lambda: handle_action(message))

    except WebSocketDisconnect:
        websocket_manager.disconnect(websocket)
