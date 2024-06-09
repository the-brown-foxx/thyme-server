from fastapi import WebSocket, WebSocketDisconnect
from reactivex import Subject

from service.authorizer.display.subject_display_controller import DisplayControllerEvent
from service.authorizer.parking.parking_space_counter import ParkingSpaceCounter
from service.registry.model.car import Car
from service.run_async import run_async


async def handle_display_controller_websocket(
        websocket: WebSocket,
        parking_space_counter: ParkingSpaceCounter,
        display_controller_subject: Subject[DisplayControllerEvent],
):
    await websocket.accept()

    vacant_space = parking_space_counter.get_parking_space_count().vacant_space
    await websocket.send_json({
        'status': 'VACANT_SPACE_UPDATE',
        'vacant_space': vacant_space,
    })

    async def on_next(event: DisplayControllerEvent):
        if event is None:
            await websocket.send_json({
                'status': 'IDLE',
                'event': 'Waiting for a car to pass',
            })
        elif isinstance(event, int):
            await websocket.send_json({
                'status': 'VACANT_SPACE_UPDATE',
                'vacant_space': event,
            })
        elif isinstance(event, Car):
            # The serializer is not working for some reason. 😁
            await websocket.send_json({
                'status': 'CAR_AUTHORIZED',
                'car': {
                    'registration_id': event.registration_id,
                    'make': event.make,
                    'model': event.model,
                    'year': event.year,
                    'color': event.color,
                    'owner': event.owner,
                }
            })
        elif isinstance(event, str):
            await websocket.send_json({
                'status': 'CAR_UNAUTHORIZED',
                'registration_id': event,
            })

    subscription = display_controller_subject.subscribe(lambda event: run_async(on_next(event)))

    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        subscription.dispose()
