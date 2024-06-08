import asyncio
from typing import Optional

from fastapi import WebSocket, WebSocketDisconnect
from pydantic import BaseModel

from service.connection.websocket_manager import WebsocketManager
from service.registry.car_registry import CarRegistry
from service.registry.model.car import Car
from sockets.exception_handler import handle_websocket_exception
from sockets.run_async import run_async


class NewCar(BaseModel):
    registration_id: str
    make: str
    model: str
    year: int
    color: str
    owner: str


class CarUpdate(BaseModel):
    registration_id: str
    make: Optional[str] = None
    model: Optional[str] = None
    year: Optional[int] = None
    color: Optional[str] = None
    owner: Optional[str] = None
    password: Optional[str] = None


async def handle_car_registry_websocket(
        websocket_manager: WebsocketManager,
        car_registry: CarRegistry,
        websocket: WebSocket,
):
    connection_successful = await websocket_manager.connect(websocket)

    if not connection_successful:
        return

    async def async_on_next_cars(cars: list[Car]):\
        await websocket_manager.broadcast({
            'action': 'show_cars',
            'cars': list(map(lambda car: car.to_dict(), cars)),
        })

    def on_next_cars(cars: list[Car]):
        run_async(async_on_next_cars(cars))

    car_registry.get_live_cars().subscribe(on_next_cars)

    def handle_action(_message: dict):
        match _message['action']:
            case 'register':
                car = NewCar.parse_obj(_message['car'])
                car_registry.register_car(car)

            case 'update':
                car_update = CarUpdate.parse_obj(_message['car'])
                car_registry.update_car(car_update)

            case 'unregister':
                car_registry.unregister_car(_message['registration_id'])

        run_async(websocket.send_json({"status": "SUCCESSFUL"}))

    try:
        while True:
            message = await websocket.receive_json()
            print(message)
            await handle_websocket_exception(websocket, lambda: handle_action(message))

    except WebSocketDisconnect:
        websocket_manager.disconnect(websocket)
